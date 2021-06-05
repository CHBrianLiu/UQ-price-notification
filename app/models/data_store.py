from app.config import app_config
from app.config.config_model import DatabaseTypeEnum
from app.models.azure_storage_blob import AzureBlob
from app.models.standard_model import IDataStore


def get_database_access() -> IDataStore:
    if app_config.DATABASE_CLASS == DatabaseTypeEnum.azure_blob:
        return AzureBlob()

data_access = get_database_access()
