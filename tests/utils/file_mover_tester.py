from memover import file_handler


class FileMoverTester:

    _SOURCE_DIRECTORY = 'sourcefolder/'
    _SHOW_DESTINATION_DIRECTORY = 'show-destination/'
    _MOVIE_DESTINATION_DIRECTORY = 'movie-destination/'

    def _create_test_dirs(self):
        file_handler.create_dir(self._SOURCE_DIRECTORY)
        file_handler.create_dir(self._SHOW_DESTINATION_DIRECTORY)
        file_handler.create_dir(self._MOVIE_DESTINATION_DIRECTORY)

    def _delete_test_dirs(self):
        file_handler.delete_directory(self._SOURCE_DIRECTORY)
        file_handler.delete_directory(self._SHOW_DESTINATION_DIRECTORY)
        file_handler.delete_directory(self._MOVIE_DESTINATION_DIRECTORY)

    def _createSourceFile(self, relative_path):
        file_path = self._SOURCE_DIRECTORY + relative_path
        file_handler.create_file(file_path)
        return file_path

    def _assert_file_moved(self, source_path, destination_path):
        file_is_in_new_path = file_handler.file_exist(destination_path)
        if not file_is_in_new_path:
            raise AssertionError('file does not exist in new path: ' + source_path)

        file_is_in_old_path = file_handler.file_exist(self._SOURCE_DIRECTORY + source_path)
        if file_is_in_old_path:
            raise AssertionError('file is still in old path')

    def _set_size_in_mb(self, file_path, size_in_mb):
        with open(self._SOURCE_DIRECTORY + file_path, 'wb') as bigfile:
            bigfile.seek(1048575 * size_in_mb)
            bigfile.write('0')
