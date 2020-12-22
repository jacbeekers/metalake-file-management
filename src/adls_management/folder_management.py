import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings

from src.adls_management import connection
from src.utils import settings


class ADLSFolderManagement:

    def __init__(self, configuration_file="resources/connection_config.json"):
        # use default connection config file
        self.settings = settings.GenericSettings(configuration_file=configuration_file)
        self.settings.get_config()

        self.service_client, self.file_system_client = connection.ConnectionManagement().create_connection(
            storage_account_name=self.settings.storage_account_name
            , storage_account_key=self.settings.storage_account_key
        )

    def create_directory(self, directory):
        try:
            self.file_system_client.create_directory(directory=directory)
        except Exception as e:
            print(e)

    def delete_directory(self, directory):
        try:
            self.file_system_client.delete_directory(directory=directory)
        except Exception as e:
            print(e)
