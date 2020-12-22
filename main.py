# Run main
from src.adls_management import folder_management


def main():
    print(__name__)
    folder="test"
    mgmt = folder_management.ADLSFolderManagement("resources/connection_config.json")
    print("Creating directory:" , folder)
    rc = mgmt.create_directory(folder)
    rc["reference"] = "create_directory for >" + folder + "<."
    print("create returned", rc)
    print("Removing directory", folder)
    rc = mgmt.delete_directory(folder)
    rc["reference"] = "delete_directory for >" + folder + "<."
    print("delete returned", rc)


if __name__ == '__main__':
    main()

