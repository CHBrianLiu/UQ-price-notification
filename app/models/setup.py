from app.config.loader import get_config_by_key
from azure.storage.blob import BlobServiceClient, PublicAccess


testing = get_config_by_key("local.testing")
azure_config = get_config_by_key("azure")
account_url = (
    (f"https://{azure_config.get('account', {}).get('name', '')}.blob.core.windows.net")
    if not testing
    else "http://127.0.0.1:10000/devstoreaccount1"
)
account_key = (
    azure_config.get("account", {}).get("access_key", "")
    if not testing
    else "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
)


def setup_azure_blob():
    blob_service_client = BlobServiceClient(
        account_url, account_key
    )
    for container in azure_config.get("blob", {}).get("containers", []):
        if not blob_service_client.get_container_client(container).exists():
            blob_service_client.create_container(
                container, public_access=PublicAccess.OFF
            )
