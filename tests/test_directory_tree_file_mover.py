import subprocess

__author__ = 'alexander'

import unittest
from directoryTreeFileMover import file_handler


class FileMatcherTest(unittest.TestCase):

    TEST_SEARCH_IN_DIRECTORY_PATH = 'sourcefolder'
    TEST_DESTINATION_ROOT_FOLDER = 'destination'

    TEST_FILE_PATH = TEST_SEARCH_IN_DIRECTORY_PATH + '/Halt.and.Catch.Fire.S02E10.720p.HDTV.x264-KILLERS.mkv'

    def setUp(self):
        file_handler.create_dir(self.TEST_SEARCH_IN_DIRECTORY_PATH)
        file_handler.create_dir(self.TEST_DESTINATION_ROOT_FOLDER)
        file_handler.create_file(self.TEST_FILE_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.TEST_SEARCH_IN_DIRECTORY_PATH)
        file_handler.delete_directory(self.TEST_DESTINATION_ROOT_FOLDER)

    def runTest(self):
        self.__run_app('"halt and catch fire" -f')

    def __run_app(self, args):
        p = subprocess.Popen('python -m directoryTreeFileMover ' + args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line,
