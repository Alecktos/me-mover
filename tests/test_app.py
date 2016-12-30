import subprocess
import unittest
from memover import file_handler


class FileMatcherTest(unittest.TestCase):

    TEST_SEARCH_IN_DIRECTORY_PATH = 'sourcefolder'
    TEST_DESTINATION_ROOT_FOLDER = 'destination'
    TEST_FILE_NAME = '/Halt.and.Catch.Fire.S02E10.720p.SOMETHING.something-SOMETHING.mkv'
    TEST_FILE_SOURCE_PATH = TEST_SEARCH_IN_DIRECTORY_PATH + TEST_FILE_NAME

    def setUp(self):
        file_handler.create_dir(self.TEST_SEARCH_IN_DIRECTORY_PATH)
        file_handler.create_dir(self.TEST_DESTINATION_ROOT_FOLDER)
        file_handler.create_file(self.TEST_FILE_SOURCE_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.TEST_SEARCH_IN_DIRECTORY_PATH)
        file_handler.delete_directory(self.TEST_DESTINATION_ROOT_FOLDER)

    def test_moving_show_by_name(self):
        self.__run_app('tvshow -show-name "halt and catch fire" -show-source sourcefolder -show-destination destination -movie-destination destination')
        self.__assert_file_in_new_path()
        self.__assert_file_not_in_old_path()

    @staticmethod
    def __run_app(args):
        p = subprocess.Popen('python -m memover ' + args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line,

    def __assert_file_in_new_path(self):
        destination_path = self.TEST_DESTINATION_ROOT_FOLDER + '/Halt And Catch Fire/Season 2' + self.TEST_FILE_NAME
        file_is_in_new_path = file_handler.check_file_existance(destination_path)
        self.assertTrue(file_is_in_new_path)

    def __assert_file_not_in_old_path(self):
        file_is_in_old_path = file_handler.check_file_existance(self.TEST_FILE_SOURCE_PATH)
        self.assertFalse(file_is_in_old_path)
