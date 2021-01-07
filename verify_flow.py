from adls_management.adls_management import folder_management
from adls_management.interface_file_management import interface_file_handling
from adls_management.batch_process_phases import from_to_phase

config_file = "resources/connection_config.json"
dummy_file = "resources/dummy.txt"


def create_directory(configuration_file=config_file, to_create=None):
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
    return rc


def verify_directory_deletion(configuration_file=config_file, to_delete="dummy.txt"):
    mgmt = folder_management.ADLSFolderManagement(configuration_file)
    print("Removing directory", to_delete)
    rc = mgmt.delete_directory(to_delete)
    rc["reference"] = "delete_directory for >" + to_delete + "<."
    print("delete returned", rc)


def copy_from_incoming_to_todo(handler):
    print(__name__)
    print("Copy the file(s) from >%s< to >%s<", (handler.settings.incoming, handler.settings.todo))
    result = handler.copy_files(from_location=handler.settings.incoming, to_location=handler.settings.todo
                                , file_pattern="*")
    print(result)
    print("5. verify the two directories contain the same files (the one that was uploaded)")
    result = handler.check_files(source_location=handler.settings.incoming, target_location=handler.settings.todo
                                 , file_pattern="*")
    return result


def prepare_incoming(handler, mgmt):
    print("upload a file to " + mgmt.settings.incoming)
    result = handler.upload_file(location=mgmt.settings.incoming, filename=dummy_file)
    return result


def main():
    batch_handler = from_to_phase.FilesBatchPhaseFromTo(configuration_file=config_file, run_id=None)
    handler = interface_file_handling.InterfaceFileHandling(
        configuration_file=config_file)
    mgmt = folder_management.ADLSFolderManagement(configuration_file=config_file)
    create_directory(configuration_file=config_file, to_create=mgmt.settings.incoming)
    create_directory(configuration_file=config_file, to_create=mgmt.settings.todo)
    result = prepare_incoming(handler, mgmt)
    print("result prepare_incoming: ", result)
    result = batch_handler.from_incoming2todo()
    print("result from_incoming2todo:", result)
    result = batch_handler.from_todo2busy()
    print("result from_todo2busy", result)
    result = batch_handler.from_busy2done()
    print("result from_busy2done", result)
    return result


if __name__ == '__main__':
    result = main()
    if result["code"] == "OK":
        exit(0)
    else:
        exit(1)
