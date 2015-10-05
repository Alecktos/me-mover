import unittest
from file_mover import FileMover
from file_handler import FileHandler


class FileMoverTest(unittest.TestCase):

    TEST_DESTINATION_DIRECTORY_ROOT = 'destination'
    TEST_DESTINATION_DIRECTORY_RELATIVE_PATH = 'destination/Heroes/Season 1/'
    TEST_SOURCE_RELATIVE_PATH = 'source/'
    TEST_FILE_RELATIVE_PATH = 'HEROES.S01E02.DVDRIP.XVID-REWRD.txt'

    def setUp(self):
        self.__file_mover = FileMover()
        self.__file_handler = FileHandler()

        self.__file_handler.create_dir(self.TEST_SOURCE_RELATIVE_PATH)
        self.__file_handler.create_dir(self.TEST_DESTINATION_DIRECTORY_RELATIVE_PATH)

    def tearDown(self):
        self.__file_handler.delete_directory(self.TEST_SOURCE_RELATIVE_PATH)
        self.__file_handler.delete_directory(self.TEST_DESTINATION_DIRECTORY_ROOT)

    def runTest(self):
        source_file_path = self.TEST_SOURCE_RELATIVE_PATH + self.TEST_FILE_RELATIVE_PATH
        self.__file_handler.create_file(source_file_path)
        self.__file_mover.move_file(source_file_path, self.TEST_DESTINATION_DIRECTORY_ROOT, 'Heroes')

        destination_path = self.TEST_DESTINATION_DIRECTORY_RELATIVE_PATH + self.TEST_FILE_RELATIVE_PATH
        self.__assert_that_file_has_been_moved(destination_path, source_file_path)
        self.__file_handler.delete_file(destination_path)

    def __assert_that_file_has_been_moved(self, destination_path, source_path):
        file_is_in_new_path = self.__file_handler.check_file_existance(destination_path)
        file_is_in_source_path = self.__file_handler.check_file_existance(source_path)

        self.assertTrue(file_is_in_new_path)
        self.assertFalse(file_is_in_source_path)

    def __remove_source_file_if_exist(self, source_file_path):
        try:
            self.__file_handler.delete_file(source_file_path)
        except:
            pass

if __name__ == '__main__':
    unittest.main()
