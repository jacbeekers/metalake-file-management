from datetime import datetime

from src.adls_management import connection
from src.utils import settings, messages
import os
from azure.core import exceptions
from azure.storage.blob import BlobClient
import time


class InterfaceFileHandling:
    right_now = datetime.now().isoformat(timespec="microseconds").replace(":", "-")

    def __init__(self, configuration_file):
        # use provided connection config file
        self.settings = settings.GenericSettings(configuration_file=configuration_file)
        self.settings.get_config()

        self.service_client, self.file_system_client, self.blob_service_client, self.container_client, self.sas_token \
            = connection.ConnectionManagement(self.settings).create_connection(
            storage_account_name=self.settings.storage_account_name
            , storage_account_key=self.settings.storage_account_key
            , container=self.settings.storage_container
        )
        self.max_wait_in_sec = 60
        self.recheck = 10
        self.tgt = None

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
            result["reference"] = "No files in source: " + from_location
            return result

        for file in sources:
            # TODO: Get a lease to prevent source file to be changed.
            # https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-copy?tabs=python
            src_file = file # os.path.basename(file)
            tgt_file = to_location + "/" + os.path.basename(src_file)
            src_blob = BlobClient(
                self.blob_service_client.url,
                container_name=self.settings.storage_container,
                blob_name=src_file,
                credential=self.sas_token
            )
            print(f"Copying %s.%s to %s using url %s" % (self.settings.storage_container, src_file, tgt_file, src_blob.url))

            #src_blob = self.blob_service_client.get_blob_client(container_name=self.settings.storage_container
            #                                                    , blob_name=src_file
            #                                                    , credential = self.sas_token)
            self.tgt = self.blob_service_client.get_blob_client(self.settings.storage_container, tgt_file)

            # download_file_path = os.path.join(".", str.replace("tryout", '.txt', 'DOWNLOAD.txt'))
            # print("\nDownloading blob to \n\t" + download_file_path)
            # with open(download_file_path, "wb") as download_file:
            #    download_file.write(src_blob.download_blob().readall())

            try:
                action = self.tgt.start_copy_from_url(src_blob.url)
                copy_id = action["copy_id"]
                status = action["copy_status"]
                error = action["error_code"]
                self.wait_condition(condition=self.check_copy_status
                                    , timeout=self.max_wait_in_sec
                                    , granularity=self.recheck)

                properties = self.tgt.get_blob_properties()
                print("Total bytes: " + str(properties.size))
                copy_props = properties.copy
                if copy_props["status"] != "success":
                    self.tgt.abort_copy(copy_id=copy_props["id"])
                    print(f"Unable to copy blob %s to %s. Status: %s" % (src_file, tgt_file, copy_props.status))
                    result = messages.message["copy_files_failed"]
                    break

                result = messages.message["ok"]
            except exceptions.ResourceNotFoundError as e:
                print("Azure reported a resource not found error: ", e)
                result = messages.message["resource_not_found"]
                result["reference"] = f"source: %s, targte: %s" % (src_file, tgt_file)

        return result

    def wait_condition(self, condition, timeout=10.0, granularity=1.0, time_factory=time):
        """
        thankfully re-used from
        https://stackoverflow.com/questions/45455898/polling-for-a-maximum-wait-time-unless-condition-in-python-2-7
        """
        end_time = time.time() + timeout  # compute the maximal end time
        status = condition()  # first condition check, no need to wait if condition already True
        while not status and time.time() < end_time:  # loop until the condition is false and timeout not exhausted
            time.sleep(granularity)  # release CPU cycles
            status = condition()  # check condition
        return status

    def check_copy_status(self):
        properties = self.tgt.get_blob_properties()
        copy_props = properties.copy
        print("properties: ", copy_props)
        # Display the copy status
        print("Copy status: " + copy_props["status"])
        # print("Copy progress: " + copy_props["progress"])
        # print("Completion time: " + str(copy_props["completion_time"]))
        if copy_props["status"] == "pending":
            done = False
        else:
            done = True
        return done

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
            result = messages.message["check_files_difference_found"]
            result["reference"] = "location >" + source_location \
                                  + "< and location >" + target_location \
                                  + "< do NOT have the same files."
        return result

    def list_files(self, location, file_pattern):
        files = []
        try:
            paths = self.file_system_client.get_paths(path=location)
            for path in paths:
                files.append(path.name)
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
        result, source_list = self.list_files(location=location, file_pattern=file_pattern)
        if result["code"] == "OK":
            for file in source_list:
                try:
                    src_blob = BlobClient(
                        self.blob_service_client.url,
                        container_name=self.settings.storage_container,
                        blob_name=file,
                        credential=self.sas_token
                    )
                    src_blob.delete_blob(delete_snapshots="include")
                    print("blob removed:", file)
                except Exception as e:
                    print("Exception on blob removal:", e)
                    result = messages.message["remove_files_failed"]
        return result
