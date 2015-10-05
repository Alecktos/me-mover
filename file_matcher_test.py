import unittest
from file_matcher import FileMatcher
from file_handler import FileHandler


class FileMatcherTest(unittest.TestCase):

    TEST_DIRECTORY_RELATIVE_PATH = 'testfolder/'
    TEST_FILE_RELATIVE_PATH = 'testfolder/The.Big.Bang.Theory.S09E01.HDTV.x264-LOL[rarbg].mp4'

    def setUp(self):
        self.__file_mather = FileMatcher()
        self.__file_handler = FileHandler()
        self.__file_handler.create_dir(self.TEST_DIRECTORY_RELATIVE_PATH)

    def tearDown(self):
        self.__file_handler.delete_directory(self.TEST_DIRECTORY_RELATIVE_PATH)

    def runTest(self):
        self.__file_handler.create_file(self.TEST_FILE_RELATIVE_PATH)
        search_for = 'The Big Bang Theory'
        file_path = self.__file_mather.search_file(search_for, self.TEST_DIRECTORY_RELATIVE_PATH)
        self.assertEqual(self.TEST_FILE_RELATIVE_PATH, file_path)
        self.__file_handler.delete_file(self.TEST_FILE_RELATIVE_PATH)

if __name__ == '__main__':
    unittest.main()
