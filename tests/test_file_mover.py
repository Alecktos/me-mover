# coding=utf-8
import os
import unittest
from episodeMover.file_mover import FileMover, CouldNotFindSeasonFolderException, \
    CouldNotFindShowFolderException
from episodeMover import file_handler


class FileMoverTest(unittest.TestCase):

    TEST_DESTINATION_DIRECTORY_ROOT = 'destination'
    TEST_SOURCE_PATH = 'source'

    TEST_FILE_NAMES_DESTINATION_DIRECTORY_PATH = TEST_DESTINATION_DIRECTORY_ROOT + '/Heroes/Season 1/'
    TEST_FILE_NAMES_FILE_1_SOURCE_PATH = TEST_SOURCE_PATH + '/HEROES.S01E03.DVDRIP.XVID-REWRD.mkv'
    TEST_FILE_NAMES_FILE_2_SOURCE_PATH = TEST_SOURCE_PATH + '/new.girl.cait.s01e04.hdtv.x264-daview.mp4'
    TEST_FILE_NAMES_FILE_3_SOURCE_PATH = TEST_SOURCE_PATH + '/HEROES.S01E02.DVDRIP.XVID-REWRD.mkv'

    TEST_SEASON_DIRECTORY_NOT_EXIST_FILE_SOURCE_PATH = TEST_SOURCE_PATH + '/Falling.Skies.S02E03.HDTV.x264-ASAP.mp4'
    TEST_SEASON_DIRECTORY_NOT_EXIST_DESTINATION_PATH = TEST_DESTINATION_DIRECTORY_ROOT + '/Falling Skies'

    TEST_SHOW_DIRECTORY_NOT_EXIST_FILE_SOURCE_PATH = TEST_SOURCE_PATH + '/Go.On.S01E17.HDTV.x264-LOL'

    TEST_FOLDER_NAMES_DESTINATION_DIRECTORY_PATH = TEST_DESTINATION_DIRECTORY_ROOT + '/abc/Season 9'
    TEST_FOLDER_NAMES_FOLDER_SOURCE_PATH = TEST_SOURCE_PATH + '/abc.S09E02.DVDRIP.XVID-REWRD'

    def setUp(self):
        self.__file_mover = FileMover()

        file_handler.create_dir(self.TEST_SOURCE_PATH)

        file_handler.create_dir(self.TEST_FILE_NAMES_DESTINATION_DIRECTORY_PATH)
        file_handler.create_file(self.TEST_FILE_NAMES_FILE_1_SOURCE_PATH)
        file_handler.create_file(self.TEST_FILE_NAMES_FILE_2_SOURCE_PATH)
        file_handler.create_file(self.TEST_FILE_NAMES_FILE_3_SOURCE_PATH)

        file_handler.create_dir(self.TEST_SEASON_DIRECTORY_NOT_EXIST_DESTINATION_PATH)
        file_handler.create_dir(self.TEST_SEASON_DIRECTORY_NOT_EXIST_FILE_SOURCE_PATH)

        file_handler.create_dir(self.TEST_FOLDER_NAMES_FOLDER_SOURCE_PATH)
        file_handler.create_dir(self.TEST_FOLDER_NAMES_DESTINATION_DIRECTORY_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.TEST_SOURCE_PATH)
        file_handler.delete_directory(self.TEST_DESTINATION_DIRECTORY_ROOT)

    def runTest(self):
        self.__test_file_names([self.TEST_FILE_NAMES_FILE_1_SOURCE_PATH])
        self.__test_file_names([self.TEST_FILE_NAMES_FILE_2_SOURCE_PATH, self.TEST_FILE_NAMES_FILE_3_SOURCE_PATH])
        self.__test_season_directory_not_exist()
        self.__test_show_directory_not_exist()
        self.__test_folder_names()

    def __test_season_directory_not_exist(self):
        with self.assertRaises(CouldNotFindSeasonFolderException):
            self.__file_mover.move_files(
                [self.TEST_SEASON_DIRECTORY_NOT_EXIST_FILE_SOURCE_PATH],
                self.TEST_DESTINATION_DIRECTORY_ROOT,
                'falling skies'
            )

    def __test_show_directory_not_exist(self):
        with self.assertRaises(CouldNotFindShowFolderException):
            self.__file_mover.move_files(
                [self.TEST_SHOW_DIRECTORY_NOT_EXIST_FILE_SOURCE_PATH],
                self.TEST_DESTINATION_DIRECTORY_ROOT,
                'Go On'
            )

    def __test_folder_names(self):
        self.__file_mover.move_files(
            [self.TEST_FOLDER_NAMES_FOLDER_SOURCE_PATH],
            self.TEST_DESTINATION_DIRECTORY_ROOT,
            'abc'
        )
        folder_name = self.TEST_FOLDER_NAMES_FOLDER_SOURCE_PATH.split('/')[-1]
        destination_path = self.TEST_FOLDER_NAMES_DESTINATION_DIRECTORY_PATH + '/' + folder_name

        folder_is_new_path = file_handler.check_directory_existance(destination_path)
        self.assertTrue(folder_is_new_path)

        folder_is_on_source_path = self.TEST_FOLDER_NAMES_FOLDER_SOURCE_PATH
        folder_is_in_source = file_handler.check_directory_existance(folder_is_on_source_path)
        self.assertFalse(folder_is_in_source)

    def __test_file_names(self, source_paths):
        self.__file_mover.move_files(source_paths, self.TEST_DESTINATION_DIRECTORY_ROOT, ' heroes')
        self.__assert_that_files_has_been_moved(source_paths)

    def __assert_that_files_has_been_moved(self, source_paths):
        for source_path in source_paths:
            file_name = os.path.basename(source_path)
            destination_path = self.TEST_FILE_NAMES_DESTINATION_DIRECTORY_PATH + file_name

            file_is_in_new_path = file_handler.check_file_existance(destination_path)
            self.assertTrue(file_is_in_new_path)

            file_is_in_source_path = file_handler.check_file_existance(source_path)
            self.assertFalse(file_is_in_source_path)