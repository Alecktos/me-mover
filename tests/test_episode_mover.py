import os
import unittest
from episodeMover.episode_mover import EpisodeMover
from episodeMover import file_handler


class FileMoverTest(unittest.TestCase):

    __DIRECTORY_ROOT = 'destination'
    __SOURCE_PATH = 'source'

    __NEW_GRIL_FILE_SOURCE_PATH = __SOURCE_PATH + '/new.girl.s01e04.something.something-something.mp4'
    __HEROES_FILE_DESTINATION_DIRECTORY_PATH = __DIRECTORY_ROOT + '/Heroes/Season 1/'
    __HEROES_FILE_1_SOURCE_PATH = __SOURCE_PATH + '/HEROES.S01E03.something.something-something.mkv'
    __HEROES_FILE_2_SOURCE_PATH = __SOURCE_PATH + '/HEROES.S01E02.something.something-something.mkv'

    __FALLING_SKIES_FILE_SOURCE_PATH = __SOURCE_PATH + '/Falling.Skies.S02E03.SOMETHING.SOMETHING-SOMETHING.mp4'

    __GO_ON_FILE_SOURCE_PATH = __SOURCE_PATH + '/Go.On.S01E17.SOMETHING.something-something'

    __ABC_SEASON_DESTINATION_DIRECTORY_PATH = __DIRECTORY_ROOT + '/abc/Season 9'
    __AABC_FILE_SOURCE_PATH = __SOURCE_PATH + '/abc.S09E02.something.something-something'

    def setUp(self):
        self.__episode_mover = EpisodeMover()

        file_handler.create_dir(self.__SOURCE_PATH)

        file_handler.create_dir(self.__HEROES_FILE_DESTINATION_DIRECTORY_PATH)
        file_handler.create_file(self.__HEROES_FILE_1_SOURCE_PATH)
        file_handler.create_file(self.__NEW_GRIL_FILE_SOURCE_PATH)
        file_handler.create_file(self.__HEROES_FILE_2_SOURCE_PATH)

        file_handler.create_file(self.__GO_ON_FILE_SOURCE_PATH)
        file_handler.create_file(self.__FALLING_SKIES_FILE_SOURCE_PATH)

        file_handler.create_dir(self.__AABC_FILE_SOURCE_PATH)
        file_handler.create_dir(self.__ABC_SEASON_DESTINATION_DIRECTORY_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_PATH)
        file_handler.delete_directory(self.__DIRECTORY_ROOT)

    def runTest(self):
        self.__test_file_names([self.__HEROES_FILE_1_SOURCE_PATH])
        self.__test_file_names([self.__NEW_GRIL_FILE_SOURCE_PATH, self.__HEROES_FILE_2_SOURCE_PATH])
        self.__test_season_directory_exist()
        self.__test_show_exist()
        self.__test_folder_names()

    def __test_season_directory_exist(self):
        self.__episode_mover.move_files(
            [self.__FALLING_SKIES_FILE_SOURCE_PATH],
            self.__DIRECTORY_ROOT,
            'falling skies'
        )
        directory_exist = file_handler.check_directory_existance(self.__DIRECTORY_ROOT + '/falling skies')
        self.assertTrue(directory_exist)

    def __test_show_exist(self):
        self.__episode_mover.move_files(
            [self.__GO_ON_FILE_SOURCE_PATH],
            self.__DIRECTORY_ROOT,
            'Go On'
        )
        directory_exist = file_handler.check_directory_existance(self.__DIRECTORY_ROOT + '/go on')
        self.assertTrue(directory_exist)

    def __test_folder_names(self):
        self.__episode_mover.move_files(
            [self.__AABC_FILE_SOURCE_PATH],
            self.__DIRECTORY_ROOT,
            'abc'
        )
        folder_name = self.__AABC_FILE_SOURCE_PATH.split('/')[-1]
        destination_path = self.__ABC_SEASON_DESTINATION_DIRECTORY_PATH + '/' + folder_name

        folder_is_new_path = file_handler.check_directory_existance(destination_path)
        self.assertTrue(folder_is_new_path)

        folder_is_on_source_path = self.__AABC_FILE_SOURCE_PATH
        folder_is_in_source = file_handler.check_directory_existance(folder_is_on_source_path)
        self.assertFalse(folder_is_in_source)

    def __test_file_names(self, source_paths):
        self.__episode_mover.move_files(source_paths, self.__DIRECTORY_ROOT, ' heroes')
        self.__assert_that_files_has_been_moved(source_paths)

    def __assert_that_files_has_been_moved(self, source_paths):
        for source_path in source_paths:
            file_name = os.path.basename(source_path)
            destination_path = self.__HEROES_FILE_DESTINATION_DIRECTORY_PATH + file_name

            file_is_in_new_path = file_handler.check_file_existance(destination_path)
            self.assertTrue(file_is_in_new_path)

            file_is_in_source_path = file_handler.check_file_existance(source_path)
            self.assertFalse(file_is_in_source_path)