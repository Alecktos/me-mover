from memover import file_handler


class FileMovedAssertion:

    def assertFileMoved(self, source_path, destination_path):
        file_is_in_new_path = file_handler.check_file_existance(destination_path)
        if not file_is_in_new_path:
            raise AssertionError('file does not exist in new path ')

        file_is_in_old_path = file_handler.check_file_existance(source_path)
        if file_is_in_old_path:
            raise AssertionError('file is still in old path')
