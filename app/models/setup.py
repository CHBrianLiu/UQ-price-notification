from app.config.loader import get_config_by_key
from azure.storage.blob import BlobServiceClient, PublicAccess


azure_config = get_config_by_key("azure")
account_url = (
    f"https://{azure_config.get('account', {}).get('name', '')}.blob.core.windows.net"
)


def setup_azure_blob():
    blob_service_client = BlobServiceClient(
        account_url, azure_config.get("account", {}).get("access_key", "")
    )
    for container in azure_config.get("blob", {}).get("containers", []):
        if not blob_service_client.get_container_client(container).exists():
            blob_service_client.create_container(
                container, public_access=PublicAccess.OFF
            )
