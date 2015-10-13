import unittest
from directoryTreeFileMover.file_matcher import FileMatcher
from directoryTreeFileMover import file_handler


class FileMatcherTest(unittest.TestCase):

    TEST_SEARCH_IN_DIRECTORY_PATH = 'testfolder'
    TEST_FILE_PATH = TEST_SEARCH_IN_DIRECTORY_PATH + '/The.Big.Bang.Theory.S09E01.HDTV.x264-LOL[rarbg].mp4'
    TEST_FOLDER_PATH = TEST_SEARCH_IN_DIRECTORY_PATH + '/hey.arnold.S09E01.HDTV.x264-LOL'

    def setUp(self):
        self.__file_mather = FileMatcher()
        file_handler.create_dir(self.TEST_SEARCH_IN_DIRECTORY_PATH)
        file_handler.create_file(self.TEST_FILE_PATH)
        file_handler.create_dir(self.TEST_FOLDER_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.TEST_SEARCH_IN_DIRECTORY_PATH)

    def runTest(self):
        self.__test_matching_file()
        self.__test_matching_folder()

    def __test_matching_file(self):
        search_for = 'The Big Bang Theory'
        file_paths = self.__file_mather.search_files(search_for, self.TEST_SEARCH_IN_DIRECTORY_PATH)
        self.assertEquals(1, len(file_paths))
        self.assertEqual(self.TEST_FILE_PATH, file_paths[0])

    def __test_matching_folder(self):
        search_for = 'hey arnold'
        file_paths = self.__file_mather.search_files(search_for, self.TEST_SEARCH_IN_DIRECTORY_PATH)
        self.assertEquals(1, len(file_paths))
        self.assertEqual(self.TEST_FOLDER_PATH, file_paths[0])
