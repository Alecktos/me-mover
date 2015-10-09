import unittest
from directoryTreeFileMover.file_mover import FileMover
from directoryTreeFileMover.file_handler import FileHandler


class FileMoverTest(unittest.TestCase):

    TEST_DESTINATION_DIRECTORY_ROOT = 'destination'
    TEST_DESTINATION_DIRECTORY_RELATIVE_PATH = 'destination/Heroes/Season 1/'
    TEST_SOURCE_RELATIVE_PATH = 'source/'

    def setUp(self):
        self.__file_mover = FileMover()
        self.__file_handler = FileHandler()

        self.__file_handler.create_dir(self.TEST_SOURCE_RELATIVE_PATH)
        self.__file_handler.create_dir(self.TEST_DESTINATION_DIRECTORY_RELATIVE_PATH)

    def tearDown(self):
        self.__file_handler.delete_directory(self.TEST_SOURCE_RELATIVE_PATH)
        self.__file_handler.delete_directory(self.TEST_DESTINATION_DIRECTORY_ROOT)

    def runTest(self):
        self.__test_file_names(['HEROES.S01E03.DVDRIP.XVID-REWRD.mkv'])
        self.__test_file_names(['i.am.cait.s01e04.hdtv.x264-daview.mp4', 'HEROES.S01E02.DVDRIP.XVID-REWRD.mkv'])

    def __test_file_names(self, file_names):
        source_file_paths = []
        for file_name in file_names:
            source_file_paths.append(self.TEST_SOURCE_RELATIVE_PATH + file_name)

        self.__create_files(source_file_paths)
        #TODO: Den ska leta upp namnet på serien utifrån sökordet bättre...
        self.__file_mover.move_files(source_file_paths, self.TEST_DESTINATION_DIRECTORY_ROOT, 'Heroes')
        self.__assert_that_files_has_been_moved(file_names)

    def __create_files(self, source_file_paths):
        for source_file_path in source_file_paths:
            self.__file_handler.create_file(source_file_path)

    def __assert_that_files_has_been_moved(self, file_names):
        for file_name in file_names:
            source_path = self.TEST_SOURCE_RELATIVE_PATH + file_name
            destination_path = self.TEST_DESTINATION_DIRECTORY_RELATIVE_PATH + file_name

            file_is_in_new_path = self.__file_handler.check_file_existance(destination_path)
            file_is_in_source_path = self.__file_handler.check_file_existance(source_path)

            self.assertTrue(file_is_in_new_path)
            self.assertFalse(file_is_in_source_path)