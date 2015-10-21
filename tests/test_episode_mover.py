import subprocess

__author__ = 'alexander'

import unittest
from episodeMover import file_handler


class FileMatcherTest(unittest.TestCase):

    TEST_SEARCH_IN_DIRECTORY_PATH = 'sourcefolder'
    TEST_DESTINATION_ROOT_FOLDER = 'destination'
    TEST_FILE_NAME = '/Halt.and.Catch.Fire.S02E10.720p.HDTV.x264-KILLERS.mkv'
    TEST_FILE_SOURCE_PATH = TEST_SEARCH_IN_DIRECTORY_PATH + TEST_FILE_NAME

    def setUp(self):
        file_handler.create_dir(self.TEST_SEARCH_IN_DIRECTORY_PATH)
        file_handler.create_dir(self.TEST_DESTINATION_ROOT_FOLDER)
        file_handler.create_file(self.TEST_FILE_SOURCE_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.TEST_SEARCH_IN_DIRECTORY_PATH)
        file_handler.delete_directory(self.TEST_DESTINATION_ROOT_FOLDER)

    def runTest(self):
        self.__run_app('-show-name "halt and catch fire" -force -source sourcefolder -destination destination')
        self.__assert_file_in_new_path()
        self.__assert_file_not_in_old_path()

    def __run_app(self, args):
        p = subprocess.Popen('python -m episodeMover ' + args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line,

    def __assert_file_in_new_path(self):
        destination_path = self.TEST_DESTINATION_ROOT_FOLDER + '/halt and catch fire/Season 2' + self.TEST_FILE_NAME
        file_is_in_new_path = file_handler.check_file_existance(destination_path)
        self.assertTrue(file_is_in_new_path)

    def __assert_file_not_in_old_path(self):
        file_is_in_old_path = file_handler.check_file_existance(self.TEST_FILE_SOURCE_PATH)
        self.assertFalse(file_is_in_old_path)
