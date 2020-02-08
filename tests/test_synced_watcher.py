import unittest

from memover import file_handler
from memover.arguments_parser import MeMoverArgs, Commands
from memover.watcher.async_watcher import SyncedWatcher
from tests.utils import file_mover_tester


class TestSyncedWatcher(unittest.TestCase, file_mover_tester.FileMoverTester):


    __auto_turn_off = 6  # in seconds
    __test_file_1 = 'kolla.S04E15.asswe.xTTT-RR[abf].mkv'
    __test_file_2 = 'kolla.S05E16.asswe.xTTT-RR[abf].mkv'
    __args = None


    def setUp(self):
        self._create_test_dirs()
        self.__args = MeMoverArgs(
            Commands.WATCH,
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY,
            self.__auto_turn_off
        )

    def tearDown(self):
        self._delete_test_dirs()

    def __get_destination_path_file_1(self):
        return f'{self._SHOW_DESTINATION_DIRECTORY}/kolla/Season 4/{self.__test_file_1}'

    def __get_destination_path_file_2(self):
        return f'{self._SHOW_DESTINATION_DIRECTORY}/kolla/Season 5/{self.__test_file_2}'

    def test_in_paths_to_move_with_file(self):
        synced_watcher = SyncedWatcher(self.__args)
        file_path = self._createSourceFile(self.__test_file_1)

        synced_watcher.on_created(file_path)
        result = synced_watcher.in_paths_to_move(file_path, self._SOURCE_DIRECTORY)
        self.assertTrue(result)

    def test_in_paths_to_move_with_dir(self):
        dir_path = f'{self._SOURCE_DIRECTORY}/test_dir'
        file_handler.create_dir(dir_path)
        file_path = f'{dir_path}/{self.__test_file_1}'
        file_handler.create_file(file_path)
        synced_watcher = SyncedWatcher(self.__args)

        synced_watcher.on_created(dir_path)
        result = synced_watcher.in_paths_to_move(file_path, self._SOURCE_DIRECTORY)
        self.assertTrue(result)

    def test_path_not_added_multiple_times(self):
        synced_watcher = SyncedWatcher(self.__args)

        dir_1 = self._create_source_dir('my_dir')
        synced_watcher.on_created(dir_1)

        file_1 = self._createSourceFile(f'my_dir/test_file.exe')
        synced_watcher.on_created(file_1)

        self.assertListEqual(synced_watcher.created_paths_to_move, [dir_1])