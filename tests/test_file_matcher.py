import unittest
from directoryTreeFileMover.file_matcher import FileMatcher
from directoryTreeFileMover.file_handler import FileHandler


class FileMatcherTest(unittest.TestCase):

    TEST_SEARCH_IN_DIRECTORY_PATH = 'testfolder'
    TEST_FILE_PATH = TEST_SEARCH_IN_DIRECTORY_PATH + 'The.Big.Bang.Theory.S09E01.HDTV.x264-LOL[rarbg].mp4'

    def setUp(self):
        self.__file_mather = FileMatcher()
        self.__file_handler = FileHandler()
        self.__file_handler.create_dir(self.TEST_SEARCH_IN_DIRECTORY_PATH)

    def tearDown(self):
        self.__file_handler.delete_directory(self.TEST_SEARCH_IN_DIRECTORY_PATH)
        self.__file_handler.create_file(self.TEST_FILE_PATH)

    def runTest(self):
        search_for = 'The Big Bang Theory'
        file_paths = self.__file_mather.search_files(search_for, self.TEST_SEARCH_IN_DIRECTORY_PATH)
        self.assertEqual(self.TEST_FILE_PATH, file_paths[0])
