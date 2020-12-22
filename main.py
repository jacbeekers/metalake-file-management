# Run main
from src.adls_management import folder_management


def main():
    print(__name__)
    mgmt = folder_management.ADLSFolderManagement("resources/connection_config.json")
    mgmt.create_directory("test")


if __name__ == '__main__':
    main()

