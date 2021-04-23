import json
from typing import List

from app.config import app_config
from azure.storage.blob import BlobType, ContainerClient

account_url = (
    (f"https://{app_config.AZURE_ACOUNT_NAME}.blob.core.windows.net")
    if not app_config.LOCAL_TESTING
    else "http://127.0.0.1:10000/devstoreaccount1"
)
account_key = (
    app_config.AZURE_ACOUNT_KEY
    if not app_config.LOCAL_TESTING
    else "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
)
container_client_factory = {
    container_name: ContainerClient(
        account_url=account_url, container_name=container_name, credential=account_key
    )
    for container_name in app_config.AZURE_BLOB_CONTAINERS
}


def get_file_from_container(container: str, file_name: str):
    client = _get_client_by_name(container)

    return client.download_blob(file_name).content_as_text()


def upload_file_to_container(
    container: str, file_name: str, content: str, overwrite: bool = True
):
    client = _get_client_by_name(container)

    client.upload_blob(
        file_name, content, blob_type=BlobType.BlockBlob, overwrite=overwrite
    )


def does_file_exist(container: str, file_name: str):
    container_client = _get_client_by_name(container)
    return container_client.get_blob_client(file_name).exists()


def get_all_users() -> List[str]:
    container_client = _get_client_by_name("users")
    files = [blob.name for blob in container_client.list_blobs()]
    return [name[:-5] for name in files]


def get_all_products() -> List[str]:
    container_client = _get_client_by_name("products")
    files = [blob.name for blob in container_client.list_blobs()]
    return [name[:-5] for name in files]


def get_price_down_products() -> List[str]:
    return json.loads(get_file_from_container("notification", "price-down.json"))


def update_price_down_products(products: List[str]):
    upload_file_to_container("notification", "price-down.json", json.dumps(products))


def _get_client_by_name(container: str) -> ContainerClient:
    return container_client_factory[container]
