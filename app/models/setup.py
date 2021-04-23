from app.config import app_config
from azure.storage.blob import BlobServiceClient

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


def setup_azure_blob():
    blob_service_client = BlobServiceClient(account_url, account_key)
    for container in app_config.AZURE_BLOB_CONTAINERS:
        if not blob_service_client.get_container_client(container).exists():
            blob_service_client.create_container(container)
