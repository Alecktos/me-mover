import subprocess
import sys
import time
import unittest

from memover import file_handler
from tests.utils import file_mover_tester


class TestWatcher(unittest.TestCase, file_mover_tester.FileMoverTester):

    __test_file_1 = 'kolla.S04E15.asswe.xTTT-RR[abf].mkv'
    __test_file_2 = 'kolla.S05E16.asswe.xTTT-RR[abf].mkv'

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    def __get_destination_path_file_1(self):
        return f'{self._SHOW_DESTINATION_DIRECTORY}/kolla/Season 4/{self.__test_file_1}'

    def __get_destination_path_file_2(self):
        return f'{self._SHOW_DESTINATION_DIRECTORY}/kolla/Season 5/{self.__test_file_2}'

    def test_moving_multiple_files(self):
        def run_app():
            args = f'{self._SOURCE_DIRECTORY} {self._SHOW_DESTINATION_DIRECTORY} {self._MOVIE_DESTINATION_DIRECTORY} --moves 2'
            execution = f'{sys.executable} -m memover watch {args}'
            p = subprocess.Popen(execution, shell=True)
            return p

        process = run_app()
        time.sleep(1)  # Run app for a second before creating files

        self._createSourceFile(self.__test_file_1)
        self._createSourceFile(self.__test_file_2)

        process.wait()

        destination_path_file_1 = self.__get_destination_path_file_1()
        file_is_in_new_path = file_handler.file_exist(destination_path_file_1)
        self.assertTrue(file_is_in_new_path)

        file_is_in_new_path = file_handler.file_exist(self.__get_destination_path_file_2())
        self.assertTrue(file_is_in_new_path)
