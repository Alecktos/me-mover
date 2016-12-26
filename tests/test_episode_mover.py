import unittest
from memover import file_handler, episode_mover


class FileMoverTest(unittest.TestCase):

    __DIRECTORY_ROOT = 'destination'
    __SOURCE_PATH = 'source'

    __NEW_GIRL_FILE_SOURCE_PATH = __SOURCE_PATH + '/new.girl.s01e04.something.something-something.mp4'
    __NEW_GIRL_FILE_DESTINATION_PATH = __DIRECTORY_ROOT + '/new girl/Season 1/new.girl.s01e04.something.something-something.mp4'

    __HEROES_FILE_1_SOURCE_PATH = __SOURCE_PATH + '/HEROES.S01E03.something.something-something.mkv'
    __HEROES_FILE_1_DESTINATION_PATH = __DIRECTORY_ROOT + '/Heroes/Season 1/HEROES.S01E03.something.something-something.mkv'

    __HEROES_FILE_2_SOURCE_PATH = __SOURCE_PATH + '/HEROES.S01E02.something.something-something.mkv'
    __HEROES_FILE_2_DESTINATION_PATH = __DIRECTORY_ROOT + '/Heroes/Season 1/HEROES.S01E02.something.something-something.mkv'

    __ABC_SEASON_DESTINATION_DIRECTORY_PATH = __DIRECTORY_ROOT + '/ABC/Season 9'
    __ABC_FILE_SOURCE_PATH = __SOURCE_PATH + '/abc.S09E02.something.something-something.mp4'
    __ABC_FILE_DESTINATION_PATH = __ABC_SEASON_DESTINATION_DIRECTORY_PATH + '/abc.S09E02.something.something-something.mp4'

    def setUp(self):
        file_handler.create_dir(self.__SOURCE_PATH)

        file_handler.create_file(self.__HEROES_FILE_1_SOURCE_PATH)
        file_handler.create_file(self.__NEW_GIRL_FILE_SOURCE_PATH)
        file_handler.create_file(self.__HEROES_FILE_2_SOURCE_PATH)
        file_handler.create_file(self.__ABC_FILE_SOURCE_PATH)

        file_handler.create_dir(self.__ABC_SEASON_DESTINATION_DIRECTORY_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_PATH)
        file_handler.delete_directory(self.__DIRECTORY_ROOT)

    def runTest(self):
        self.__test_moving_files([self.__HEROES_FILE_1_SOURCE_PATH], [self.__HEROES_FILE_1_DESTINATION_PATH])
        self.__test_moving_files(
            [self.__NEW_GIRL_FILE_SOURCE_PATH, self.__HEROES_FILE_2_SOURCE_PATH],
            [self.__NEW_GIRL_FILE_DESTINATION_PATH, self.__HEROES_FILE_2_DESTINATION_PATH])

        self.__test_moving_files(
            [self.__ABC_FILE_SOURCE_PATH],
            [self.__ABC_FILE_DESTINATION_PATH])  # test where season dir already exist

    def __test_moving_files(self, source_paths, destination_paths):
        episode_mover.move_files(source_paths, self.__DIRECTORY_ROOT)
        self.__assert_that_files_has_been_moved(source_paths, destination_paths)

    def __assert_that_files_has_been_moved(self, source_paths, destination_paths):
        for index, source_path in enumerate(source_paths):
            file_is_in_new_path = file_handler.check_file_existance(destination_paths[index])
            self.assertTrue(file_is_in_new_path)

            file_is_not_in_source_path = file_handler.check_file_existance(source_path)
            self.assertFalse(file_is_not_in_source_path)
