from datetime import datetime

from src.adls_management import connection, messages
from src.utils import settings


class InterfaceFileHandling:
    right_now = datetime.now().isoformat(timespec="microseconds").replace(":", "-")

    def __init__(self, configuration_file):
        # use provided connection config file
        self.settings = settings.GenericSettings(configuration_file=configuration_file)
        self.settings.get_config()

        self.service_client, self.file_system_client, self.blob_service_client \
            = connection.ConnectionManagement(self.settings).create_connection(
            storage_account_name=self.settings.storage_account_name
            , storage_account_key=self.settings.storage_account_key
            , container=self.settings.storage_container
        )

    def move_files(self, from_location, to_location, file_pattern):
        result = self.copy_files(from_location=from_location, to_location=to_location, file_pattern=file_pattern)
        if result == messages.message["ok"]:
            result = self.remove_files(location=from_location, file_pattern=file_pattern)

        return result

    def copy_files(self, from_location, to_location, file_pattern):
        result = messages.message["copy_files_failed"]
        result, sources = self.list_files(location=from_location, file_pattern=file_pattern)
        if sources is None:
            print("no files found in source >" + from_location + "<.")
            result = messages.message["ok"]
            result["reference"] = "No files in source."
            return result

        for file in sources:
            src_file = from_location + "/" + file
            src = self.blob_service_client.get_blob_client(src_file)
            tgt_file = to_location + "/" + file
            tgt = self.blob_service_client.get_blob_client(tgt_file)
            tgt.start_copy_from_ulr(src.url, requires_sync=True)
            copy_properties = tgt.get_blob_properties().copy
            if copy_properties.status != "success":
                tgt.abort_copy(copy_properties.id)
                print(f"Unable to copy blob %s to %s. Status: %s" % (src_file, tgt_file, copy_properties.status))
                result = messages.message["copy_files_failed"]
                break
            result = messages.message["ok"]

        return result

    def check_files(self, source_location, target_location, file_pattern):
        """
            source and target must have the same files (simple list comparison)
        """
        result, source_list = self.list_files(location=source_location, file_pattern=file_pattern)
        result, target_list = self.list_files(location=target_location, file_pattern=file_pattern)
        if source_list == target_list:
            result = messages.message["ok"]
            result["reference"] = "location >" + source_location \
                                  + "< and location >" + target_location \
                                  + "< have the same files."
        else:
            result = messages.message["difference found"]
            result["reference"] = "location >" + source_location \
                                  + "< and location >" + target_location \
                                  + "< do NOT have the same files."
        return result

    def list_files(self, location, file_pattern):
        files = []
        try:
            paths = self.file_system_client.get_paths(path=location)
            for path in paths:
                files.append(path)
            result = messages.message["ok"]
        except Exception as e:
            print(e)
            result = messages.message["list_directory_error"]
            result["reference"] = "directory: " + location
            return result, None
        return result, files

    def historize_files(self, source_location, file_pattern, recursive=True):
        return

    def remove_files(self, location, file_pattern):
        result = messages.message["remove_files_failed"]
        return result
