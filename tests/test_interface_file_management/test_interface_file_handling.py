from adls_management.interface_file_management import interface_file_handling
from adls_management.adls_management import folder_management
import uuid


class TestInterfaceFileManagement:

    def test_list_files(self):
        handler = interface_file_handling.InterfaceFileHandling(configuration_file="tests/resources/connection_config.json")
        mgmt = folder_management.ADLSFolderManagement(configuration_file="tests/resources/connection_config.json")
        folder="test-list-files"
        mgmt.create_directory(folder)
        result, files, filenames = handler.list_files(folder, "*")
        # assert files is not None
        assert result["code"] == "OK"
        mgmt.delete_directory(folder)

    def test_check_files(self):
        self.handler = interface_file_handling.InterfaceFileHandling(
            configuration_file="tests/resources/connection_config.json")
        mgmt = folder_management.ADLSFolderManagement(configuration_file="tests/resources/connection_config.json")
        source_folder=str(uuid.uuid4()) + "test-source"
        mgmt.create_directory(source_folder)
        target_folder=str(uuid.uuid4()) + "test-target"
        mgmt.create_directory(target_folder)
        # both will be empty, so equal
        result = self.handler.check_files(source_location=source_folder, target_location=target_folder, file_pattern="*")
        assert result["code"] == "OK"
        mgmt.delete_directory(source_folder)
        mgmt.delete_directory(target_folder)

    def test_copy_files(self):
        self.handler = interface_file_handling.InterfaceFileHandling(
            configuration_file="tests/resources/connection_config.json")
        mgmt = folder_management.ADLSFolderManagement(configuration_file="tests/resources/connection_config.json")
        source_folder = "test-source"
        mgmt.create_directory(source_folder)
        target_folder = "test-target"
        mgmt.create_directory(target_folder)
        result = self.handler.copy_files(from_location=source_folder, to_location=target_folder, file_pattern="*")
        assert result["code"] == "OK"
