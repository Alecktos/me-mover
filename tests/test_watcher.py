import os
import time
import unittest
import subprocess
import sys

from memover import file_handler
from memover.watcher import SyncedWatcher
from tests.utils import file_mover_tester


class TestWatcher(unittest.TestCase, file_mover_tester.FileMoverTester):

    auto_turn_off = 4  # in seconds
    test_file_1 = 'kolla.S04E15.asswe.xTTT-RR[abf].mkv'
    test_file_2 = 'kolla.S05E16.asswe.xTTT-RR[abf].mkv'

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    def __get_destination_path_file_1(self):
        return f'{self._SHOW_DESTINATION_DIRECTORY}/kolla/Season 4/{self.test_file_1}'

    def __get_destination_path_file_2(self):
        return f'{self._SHOW_DESTINATION_DIRECTORY}/kolla/Season 5/{self.test_file_2}'

    def test_moving_application(self):
        process = self.__run_app()
        time.sleep(1)

        self._createSourceFile(self.test_file_1)

        self._createSourceFile(self.test_file_2)

        for line in process.stdout.readlines():
            print(line)

        process.wait()

        file_is_in_new_path = file_handler.file_exist(self.__get_destination_path_file_1())
        self.assertTrue(file_is_in_new_path)

        file_is_in_new_path = file_handler.file_exist(self.__get_destination_path_file_2())
        self.assertTrue(file_is_in_new_path)

    def test_path_in_paths_to_move_with_file(self):
        synced_watcher = SyncedWatcher()
        file_path = self._createSourceFile(self.test_file_1)

        synced_watcher.add_path_to_move(file_path)
        result = synced_watcher.path_in_paths_to_move(file_path, self._SOURCE_DIRECTORY)
        self.assertTrue(result)

    def test_path_in_paths_to_move_with_dir(self):
        dir_path = f'{self._SOURCE_DIRECTORY}/test_dir'
        file_handler.create_dir(dir_path)
        file_path = f'{dir_path}/{self.test_file_1}'
        file_handler.create_file(file_path)
        synced_watcher = SyncedWatcher()

        synced_watcher.add_path_to_move(dir_path)
        result = synced_watcher.path_in_paths_to_move(file_path, self._SOURCE_DIRECTORY)
        self.assertTrue(result)


    def __run_app(self):
        args = f'{self._SOURCE_DIRECTORY} {self._SHOW_DESTINATION_DIRECTORY} {self._MOVIE_DESTINATION_DIRECTORY} -q {self.auto_turn_off}'
        execution = f'{sys.executable} -m memover watch {args}'
        p = subprocess.Popen(execution, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p
