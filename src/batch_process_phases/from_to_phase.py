from src.utils import messages
from src.interface_file_management import interface_file_handling
from datetime import datetime, date
from uuid import uuid4
from src.adls_management import folder_management
from os import path


class FilesBatchPhaseFromTo:
    """
        Convenience modules to move files from one stage to the next.
        locations need to be configured in resources/locations.json (default)
    """
    right_now = datetime.now().isoformat(timespec="microseconds").replace(":", "-")
    todays_date = datetime.today().strftime("%Y-%m-%d")

    def __init__(self, configuration_file, run_id=None):
        self.run_id = None
        self.run_id, self.time_id = self.determine_run_id()
        print("run_id is >%s< with time_stamp >%s<" % (self.run_id, self.time_id))
        self.result = messages.message["ok"]
        self.file_handler = interface_file_handling.InterfaceFileHandling(configuration_file=configuration_file)
        self.folder_handler = folder_management.ADLSFolderManagement(configuration_file=configuration_file)

    def determine_run_id(self):
        if self.run_id is None:
            the_run_id = str(uuid4())
        else:
            the_run_id = self.run_id
        return the_run_id, self.right_now

    def determine_target_name(self, base_name):
        return path.join(base_name, self.todays_date, self.right_now + "--" + self.run_id)

    def from_incoming2todo(self):
        """
            Move the files to 'todo' so they can be processed. The 'incoming' is freed-up for new files.
        """
        result, files = self.file_handler.list_files(location=self.file_handler.settings.incoming, file_pattern="*")
        if result["code"] == "OK":
            if len(files) > 0:
                todo_directory = self.determine_target_name(self.file_handler.settings.todo)
                result = self.folder_handler.create_directory(directory=todo_directory)
                if result["code"] == "OK":
                    result = self.file_handler.move_files(from_location=self.file_handler.settings.incoming
                                                  , to_location=todo_directory
                                                  , file_pattern="*")
                else:
                    print("Failed to create target directory >%s<. Error: %s" % (todo_directory, result["code"]))
            else:
                print("No files in source:", self.file_handler.settings.incoming)

        return result

    def from_todo2busy(self):
        """
            Move the files to 'busy' as pre-processing step of the actual processing
        """
        return

    def from_busy2done(self):
        return

    def from_done2hist(self):
        """
            Moves files from 'done' to 'hist', where 'hist' could be a cold location
            Use this on a regular basis to clean-up the 'done' folder
        """
        # TODO: Implement
        return

    def from_busy2redo(self):
        """
            When an error occurred use this method to move the files to the configured 'redo'
        """
        # TODO: Implement
        return

    def from_to(self, from_location, to_location):
        """
            Move files from the configured from_location to the configured to_location (check locations.json)
        """
        # TODO: Implement
        return

    def free_from_to(self, from_location, to_location):
        """
            Move files from any location to any location (does not use locations.json)
        """
        # TODO: Implement
        return
