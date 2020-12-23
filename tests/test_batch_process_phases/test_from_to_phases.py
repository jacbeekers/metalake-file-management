from src.batch_process_phases import from_to_phase
from src.interface_file_management import interface_file_handling
from uuid import UUID


class TestFromToPhases:
    def test_determine_run_id(self):
        from_to = from_to_phase.FilesBatchPhaseFromTo(
            configuration_file="tests/resources/connection_config.json"
            , run_id=None)
        the_run, the_time = from_to.determine_run_id()
        print("run_id is >%s< with time_id >%s<" % (the_run, the_time))
        assert UUID(str(the_run), version=4)

    def test_from_incoming2todo(self):
        from_to = from_to_phase.FilesBatchPhaseFromTo(
            configuration_file="tests/resources/connection_config.json"
            , run_id=None)
        result = from_to.from_incoming2todo()
        assert result["code"] == "OK"
        file_handler = interface_file_handling.InterfaceFileHandling(
            configuration_file="tests/resources/connection_config.json"
        )
        result, files = file_handler.list_files(location=from_to.file_handler.settings.incoming, file_pattern="*")
        assert result["code"] == "OK"
        assert len(files) == 0
