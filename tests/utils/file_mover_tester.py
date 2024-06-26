from memover import file_handler
import os

class FileMoverTester:

    @property
    def _SOURCE_DIRECTORY(self):
        return f'{self._WORKING_DIRECTORY}/sourcefolder/'

    @property
    def _SHOW_DESTINATION_DIRECTORY(self):
        return f'{self._WORKING_DIRECTORY}/show-destination/'
    
    @property
    def _MOVIE_DESTINATION_DIRECTORY(self):
        return f'{self._WORKING_DIRECTORY}/movie-destination/'

    @property
    def _WORKING_DIRECTORY(self):
        return os.getcwd()

    def _create_test_dirs(self):
        self._delete_test_dirs()
        file_handler.create_dir(self._SOURCE_DIRECTORY)
        file_handler.create_dir(self._SHOW_DESTINATION_DIRECTORY)
        file_handler.create_dir(self._MOVIE_DESTINATION_DIRECTORY)

    def _delete_test_dirs(self):
        if file_handler.path_is_directory(self._SOURCE_DIRECTORY):
            file_handler.delete_directory(self._SOURCE_DIRECTORY)
        if file_handler.path_is_directory(self._SHOW_DESTINATION_DIRECTORY):
            file_handler.delete_directory(self._SHOW_DESTINATION_DIRECTORY)
        if file_handler.path_is_directory(self._MOVIE_DESTINATION_DIRECTORY):
            file_handler.delete_directory(self._MOVIE_DESTINATION_DIRECTORY)

    def _createSourceFile(self, relative_path):
        file_path = self._SOURCE_DIRECTORY + relative_path
        file_handler.create_file(file_path)
        return file_path

    def _create_source_dir(self, relative_path):
        dir_path = f'{self._SOURCE_DIRECTORY}{relative_path}'
        file_handler.create_dir(dir_path)
        return dir_path

    def _assert_file_moved(self, source_path, destination_path):
        file_is_in_new_path = file_handler.file_exist(destination_path)
        if not file_is_in_new_path:
            raise AssertionError('file does not exist in new path: ' + source_path)

        edited_source_path = source_path
        if self._SOURCE_DIRECTORY not in edited_source_path:
            edited_source_path = self._SOURCE_DIRECTORY + source_path

        file_is_in_old_path = file_handler.file_exist(edited_source_path)
        if file_is_in_old_path:
            raise AssertionError('file is still in old path')

    def _set_size_in_mb(self, file_path, size_in_mb):
        with open(self._SOURCE_DIRECTORY + file_path, 'wb') as bigfile:
            bigfile.seek(1048575 * size_in_mb)
            bigfile.write(b"\0")
