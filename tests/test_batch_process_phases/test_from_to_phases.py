from src.batch_process_phases import from_to_phase
from src.interface_file_management import interface_file_handling
from src.adls_management import folder_management
from uuid import UUID
from datetime import datetime, timedelta


class TestFromToPhases:

    configuration_file = "tests/resources/connection_config.json"
    prefix = "test/"

    def test_determine_run_id(self):
        from_to = from_to_phase.FilesBatchPhaseFromTo(
            configuration_file=self.configuration_file
            , run_id=None)
        the_run, the_time = from_to.determine_run_id()
        print("run_id is >%s< with time_id >%s<" % (the_run, the_time))
        assert UUID(str(the_run), version=4)

    def test_from_incoming2todo(self):
        from_to = from_to_phase.FilesBatchPhaseFromTo(
            configuration_file=self.configuration_file
            , run_id=None)
        result = from_to.from_incoming2todo()
        assert result["code"] == "OK" or result["code"] == "MLU-FH-009"
        file_handler = interface_file_handling.InterfaceFileHandling(
            configuration_file=self.configuration_file
        )
        result, files, filenames = file_handler.list_files(location=from_to.file_handler.settings.incoming, file_pattern="*")
        assert result["code"] == "OK"

    def test_from_todo2busy(self):
        from_to = from_to_phase.FilesBatchPhaseFromTo(
            configuration_file=self.configuration_file
            , run_id=None)
        # first move files from incoming to todo
        self.test_from_incoming2todo()
        result = from_to.from_todo2busy()
        assert result["code"] == "OK" or result["code"] == "MLU-FH-008"
        file_handler = interface_file_handling.InterfaceFileHandling(
            configuration_file=self.configuration_file
        )
        result, files, filenames = file_handler.list_files(location=from_to.file_handler.settings.busy, file_pattern="*")
        assert len(files) >= 0
        assert result["code"] == "OK"

    def test_determine_oldest_folder(self):
        from_to = from_to_phase.FilesBatchPhaseFromTo(self.configuration_file
            , run_id=None)
        mgmt = folder_management.ADLSFolderManagement(configuration_file=self.configuration_file)
        the_time = datetime.now()
        the_time1 = (the_time - timedelta(hours=2)).isoformat(timespec="microseconds").replace(':','-')
        mgmt.create_directory(self.prefix + the_time1)
        the_time2 = (the_time - timedelta(hours=1)).isoformat(timespec="microseconds").replace(':','-')
        mgmt.create_directory(self.prefix + the_time2)
        the_time3 = the_time.isoformat(timespec="microseconds").replace(':','-')
        mgmt.create_directory(self.prefix + the_time3)

        oldest, oldest_name = from_to.determine_oldest_folder(base_folder=self.prefix)
        print("oldest: %d location: %s" % (oldest, oldest_name))
        # cleanup
        mgmt.delete_directory(self.prefix + the_time1)
        mgmt.delete_directory(self.prefix + the_time2)
        mgmt.delete_directory(self.prefix + the_time3)
        assert oldest_name != "not_found"
