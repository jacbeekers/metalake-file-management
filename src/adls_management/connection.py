import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from src.utils import settings


class ConnectionManagement:

    def __init__(self, configuration_file="resources/connection_config.json"):
        self.service_client = None
        self.file_system_client = None
        self.settings = settings.GenericSettings(configuration_file=configuration_file)
        self.settings.get_config()

    def create_connection(self, storage_account_name, storage_account_key):
        if self.settings.azure_http_proxy is None:
            os.environ["http_proxy"] = "None"
        else:
            os.environ["http_proxy"] = self.settings.azure_http_proxy
        if self.settings.azure_https_proxy is None:
            os.environ["https_proxy"] = "None"
        else:
            os.environ["https_proxy"] = self.settings.azure_https_proxy

        try:
            self.service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
                "https", storage_account_name), credential=storage_account_key)
            self.file_system_client = self.service_client.get_file_system_client(file_system=self.settings.storage_container)
            return self.service_client, self.file_system_client

        except Exception as e:
            print(e)
            return None, None
