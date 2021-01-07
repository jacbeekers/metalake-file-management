from metalake_management.adls_management import folder_management
from metalake_management.interface_file_management import interface_file_handling

folder = "verification"
source_folder = folder + "_source"
target_folder = folder + "_target"
dummy_file = "resources/dummy.txt"


def verify_directory_creation(configuration_file="resources/connection_config.json", to_create=folder):
    """
        Configuration and access verification
            create and delete folder "verification"
    """
    print(__name__)
    mgmt = folder_management.ADLSFolderManagement(configuration_file)
    print("Creating directory:" , to_create)
    rc = mgmt.create_directory(to_create)
    rc["reference"] = "create_directory for >" + to_create + "<."
    print("create returned", rc)


def verify_directory_deletion(configuration_file="resources/connection_config.json", to_delete=folder):
    mgmt = folder_management.ADLSFolderManagement(configuration_file)
    print("Removing directory", folder)
    rc = mgmt.delete_directory(folder)
    rc["reference"] = "delete_directory for >" + to_delete + "<."
    print("delete returned", rc)


def verify_copy_files(configuration_file="resources/connection_config.json"):
    print(__name__)
    print("Overview of the verification steps:")
    print("1. create two verification directories")
    print("2. verify these are the same (empty)")
    print("3. upload a file")
    print("4. copy the file")
    print("5. verify the two directories contain the same files (the one that was uploaded)")
    print("=== Executing verification ===")
    handler = interface_file_handling.InterfaceFileHandling(
        configuration_file="resources/connection_config.json")
    mgmt = folder_management.ADLSFolderManagement(configuration_file)
    print("1. create two verification directories")
    print("\tsource_folder: " + source_folder)
    mgmt.create_directory(source_folder)
    print("\ttarget_folder: " + target_folder)
    mgmt.create_directory(target_folder)
    print("3. upload a file")
    handler.upload_file(source_folder,dummy_file)
    print("4. copy the file(s)")
    result = handler.copy_files(from_location=source_folder, to_location=target_folder, file_pattern="*")
    print(result)
    print("5. verify the two directories contain the same files (the one that was uploaded)")
    result = handler.check_files(source_location=source_folder, target_location=target_folder, file_pattern="*")
    print(result)
    print("=== Cleanup ===")
    print("\tremoving " + source_folder)
    mgmt.delete_directory(source_folder)
    print("\tremoving " + target_folder)
    mgmt.delete_directory(target_folder)


if __name__ == '__main__':
    # create a verification directory
    verify_directory_creation("resources/connection_config.json")
    # delete it
    verify_directory_deletion("resources/connection_config.json")
    verify_copy_files("resources/connection_config.json")
