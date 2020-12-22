import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from src.utils import settings
from azure.storage.blob import BlobServiceClient


class ConnectionManagement:

    def __init__(self, settings):
        self.service_client = None
        self.file_system_client = None
        self.settings = settings
        self.blob_service_client = None

    def create_connection(self, storage_account_name, storage_account_key, container):
        try:
            dfs_url="{}://{}.dfs.core.windows.net".format("https", storage_account_name)
            blob_url="{}://{}.blob.core.windows.net/".format("https", storage_account_name)
            print("ADLS URL:", dfs_url)
            print("Blob URL:", blob_url)
            # not secure: print("account key:", storage_account_key)
            print("Getting service_client...")
            self.service_client = DataLakeServiceClient(account_url=dfs_url, credential=storage_account_key)
            print("Getting file_system_client...")
            self.file_system_client = self.service_client.get_file_system_client(
                file_system=self.settings.storage_container
            )
            print("Getting blob_service_client...")
            connect_string="DefaultEndpointsProtocol=https;AccountName=" + storage_account_name + "AccountKey="\
                           + storage_account_key + ";EndpointSuffix=core.windows.net"
            self.blob_service_client = BlobServiceClient.from_connection_string(
                    conn_str=connect_string
                ).get_container_client(container)
            print("returning references.")
            return self.service_client, self.file_system_client, self.blob_service_client

        except Exception as e:
            print(e)
            return None, None, None
