import time
import unittest
import subprocess
import sys

from memover import file_handler
from memover.arguments_parser import MeMoverArgs, Commands
from memover.watcher.async_watcher import SyncedWatcher
from tests.utils import file_mover_tester

class TestWatcher(unittest.TestCase, file_mover_tester.FileMoverTester):


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

    def test_moving_multiple_files(self):
        def run_app():
            args = f'{self._SOURCE_DIRECTORY} {self._SHOW_DESTINATION_DIRECTORY} {self._MOVIE_DESTINATION_DIRECTORY} -q {self.__auto_turn_off}'
            execution = f'{sys.executable} -m memover watch {args}'
            p = subprocess.Popen(execution, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            return p

        process = run_app()
        time.sleep(1)

        self._createSourceFile(self.__test_file_1)
        self._createSourceFile(self.__test_file_2)

        for line in process.stdout.readlines():
            print(line)

        process.wait()

        file_is_in_new_path = file_handler.file_exist(self.__get_destination_path_file_1())
        self.assertTrue(file_is_in_new_path)

        file_is_in_new_path = file_handler.file_exist(self.__get_destination_path_file_2())
        self.assertTrue(file_is_in_new_path)
