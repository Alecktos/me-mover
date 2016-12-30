import unittest
from memover import file_handler, file_matcher


class FileMatcherTest(unittest.TestCase):

    __SOURCE_DIRECTORY_PATH = 'testfolder'
    __TV_SHOW_1_FILE_PATH = __SOURCE_DIRECTORY_PATH + '/The.Big.Bang.Theory.S09E01.something.something-something[something].mp4'
    __TV_SHOW_2_FOLDER_PATH = __SOURCE_DIRECTORY_PATH + '/hey.arnold.S09E01.SOMETHING.something-something'

    def setUp(self):
        file_handler.create_dir(self.__SOURCE_DIRECTORY_PATH)
        file_handler.create_file(self.__TV_SHOW_1_FILE_PATH)
        file_handler.create_dir(self.__TV_SHOW_2_FOLDER_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_DIRECTORY_PATH)

    def runTest(self):
        self.__test_matching_file()
        self.__test_matching_folder()

    def __test_matching_files(self):
        search_for = 'The Big Bang Theory'
        file_paths = file_matcher.search_files(search_for, self.__SOURCE_DIRECTORY_PATH)
        self.assertEquals(1, len(file_paths))
        self.assertEqual(self.__TV_SHOW_1_FILE_PATH, file_paths[0])

    def __test_matching_folder(self):
        search_for = 'hey arnold'
        file_paths = file_matcher.search_files(search_for, self.__SOURCE_DIRECTORY_PATH)
        self.assertEquals(1, len(file_paths))
        self.assertEqual(self.__TV_SHOW_2_FOLDER_PATH, file_paths[0])
