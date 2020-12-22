Module interface_file_management.interface_file_handling
========================================================

Classes
-------

`InterfaceFileHandling(configuration_file)`
:   

    ### Class variables

    `right_now`
    :

    ### Methods

    `check_files(self, source_location, target_location, file_pattern)`
    :   source and target must have the same files (simple list comparison)

    `copy_files(self, from_location, to_location, file_pattern)`
    :

    `historize_files(self, source_location, file_pattern, recursive=True)`
    :

    `list_files(self, location, file_pattern)`
    :

    `move_files(self, from_location, to_location, file_pattern)`
    :

    `remove_files(self, location, file_pattern)`
    :