import unittest
from memover import file_handler, file_matcher


class TestFileMatcher(unittest.TestCase):

    __SOURCE_DIRECTORY_PATH = 'testfolder'

    def setUp(self):
        file_handler.create_dir(self.__SOURCE_DIRECTORY_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_DIRECTORY_PATH)

    def runTest(self):
        self.__test_matching_file()
        self.__test_matching_file_in_folder()

    def __test_matching_file(self):
        file_path = self.__SOURCE_DIRECTORY_PATH + '/An.Other.Show.Info.S09E01.something.something-something[something].mp4'
        file_handler.create_file(file_path)

        search_for = 'An Other Show Info'
        file_paths = file_matcher.search_files(search_for, self.__SOURCE_DIRECTORY_PATH)
        self.assertEqual(1, len(file_paths))
        self.assertEqual(file_path, file_paths[0])

    def __test_matching_file_in_folder(self):
        folder_path = self.__SOURCE_DIRECTORY_PATH + '/hey.arnold.S09E01.SOMETHING.something-something'
        file_handler.create_dir(folder_path)
        search_for = 'hey arnold'

        file_paths = file_matcher.search_files(search_for, self.__SOURCE_DIRECTORY_PATH)
        self.assertEqual(1, len(file_paths))
        self.assertEqual(folder_path, file_paths[0])
