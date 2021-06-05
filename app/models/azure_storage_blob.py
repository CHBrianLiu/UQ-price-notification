import json
from typing import Dict, List

from azure.storage.blob import BlobType, ContainerClient, BlobServiceClient

from app.config import app_config
from app.models.standard_model import IDataStore
from app.models.Product import Product
from app.models.User import User


class AzureBlob(IDataStore):

    account_url: str
    account_key: str
    container_client_factory: Dict[str, ContainerClient]

    user_container: str = "users"
    product_container: str = "products"
    notification_container: str = "notification"

    price_down_product_list: str = "price-down.json"

    def __init__(self) -> None:
        self._credential_setup()
        self._setup_azure_blob()
        self._container_factory_setup()

    def has_user(self, user_id: str) -> bool:
        container_client = self._get_client_by_name(self.user_container)
        return container_client.get_blob_client(
            self._get_user_record_name_by_id(user_id)
        ).exists()

    def get_user_info(self, user_id: str) -> User:
        client = self._get_client_by_name(self.user_container)
        raw_data = client.download_blob(
            self._get_user_record_name_by_id(user_id)
        ).content_as_text()
        return User.parse_raw(raw_data)

    def update_user(self, user: User):
        client = self._get_client_by_name(self.user_container)
        client.upload_blob(
            self._get_user_record_name_by_id(user.user_id),
            user.json(),
            blob_type=BlobType.BlockBlob,
            overwrite=True,
        )

    def is_product_tracked_by_any_user(self, product_id: str) -> bool:
        container_client = self._get_client_by_name(self.product_container)
        return container_client.get_blob_client(
            self._get_user_record_name_by_id(product_id)
        ).exists()

    def get_product_info(self, product_id: str) -> Product:
        client = self._get_client_by_name(self.product_container)
        raw_data = client.download_blob(
            self._get_product_record_name_by_id(product_id)
        ).content_as_text()
        return Product.parse_raw(raw_data)

    def update_product(self, product: Product):
        client = self._get_client_by_name(self.product_container)
        client.upload_blob(
            self._get_product_record_name_by_id(product.product_id),
            product.json(),
            blob_type=BlobType.BlockBlob,
            overwrite=True,
        )

    def get_all_user_ids(self) -> List[str]:
        container_client = self._get_client_by_name(self.user_container)
        files = [blob.name for blob in container_client.list_blobs()]
        return [name[:-5] for name in files]  # get rid of .json

    def get_all_tracked_product_ids(self) -> List[str]:
        container_client = self._get_client_by_name(self.product_container)
        files = [blob.name for blob in container_client.list_blobs()]
        return [name[:-5] for name in files]  # get rid of .json

    def get_all_price_down_product_ids(self) -> List[str]:
        client = self._get_client_by_name(self.notification_container)
        raw_data = client.download_blob(self.price_down_product_list).content_as_text()
        return json.loads(raw_data)

    def update_price_down_product_list(self, product_ids: List[str]):
        client = self._get_client_by_name(self.notification_container)
        client.upload_blob(
            self.price_down_product_list,
            json.dumps(product_ids),
            blob_type=BlobType.BlockBlob,
            overwrite=True,
        )

    def _credential_setup(self):
        self.account_url = (
            (f"https://{app_config.AZURE_ACCOUNT_NAME}.blob.core.windows.net")
            if not app_config.LOCAL_TESTING
            else "http://127.0.0.1:10000/devstoreaccount1"
        )
        self.account_key = (
            app_config.AZURE_ACCOUNT_KEY
            if not app_config.LOCAL_TESTING
            else "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
        )

    def _container_factory_setup(self):
        self.container_client_factory = {
            container_name: ContainerClient(
                account_url=self.account_url,
                container_name=container_name,
                credential=self.account_key,
            )
            for container_name in (
                self.user_container,
                self.product_container,
                self.notification_container,
            )
        }

    def _setup_azure_blob(self) -> None:
        blob_service_client = BlobServiceClient(self.account_url, self.account_key)
        for container in (
            self.user_container,
            self.product_container,
            self.notification_container,
        ):
            if not blob_service_client.get_container_client(container).exists():
                blob_service_client.create_container(container)

    def _get_client_by_name(self, container: str) -> ContainerClient:
        return self.container_client_factory[container]

    def _get_user_record_name_by_id(self, user_id: str) -> str:
        return f"{user_id}.json"

    def _get_product_record_name_by_id(self, product_id: str) -> str:
        return f"{product_id}.json"
