import unittest
from memover import file_handler, mover


class MoverTest(unittest.TestCase):

    __SOURCE_DIRECTORY_PATH = 'sourcefolder'
    __SHOW_DESTINATION_ROOT_FOLDER = 'destination_show'
    __MOVIE_DESTINATION_ROOT_FOLDER = 'destination_movie'
    __TV_SHOW_FILE_NAME_1 = 'Halt.and.Catch.Fire.S02E10.720p.SOMETHING.something-SOMETHING.mkv'
    __TV_SHOW_FILE_NAME_2 = 'The.Last.Man.on.Earth.S02E03.Dead.Man.Walking.720p.WEB-DL.x123.BBA.mp4'
    __MOVIE_FILE_NAME_1 = 'Fantastic Beast and Where To Find Them 2016 HD-TS x264-CPG.mkv'

    def setUp(self):
        file_handler.create_dir(self.__MOVIE_DESTINATION_ROOT_FOLDER)
        file_handler.create_dir(self.__SHOW_DESTINATION_ROOT_FOLDER)
        file_handler.create_dir(self.__SOURCE_DIRECTORY_PATH)
        file_handler.create_file(self.__SOURCE_DIRECTORY_PATH + '/' + self.__TV_SHOW_FILE_NAME_1)
        file_handler.create_file(self.__SOURCE_DIRECTORY_PATH + '/' + self.__TV_SHOW_FILE_NAME_2)
        file_handler.create_file(self.__SOURCE_DIRECTORY_PATH + '/' + self.__MOVIE_FILE_NAME_1)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_DIRECTORY_PATH)
        file_handler.delete_directory(self.__SHOW_DESTINATION_ROOT_FOLDER)
        file_handler.delete_directory(self.__MOVIE_DESTINATION_ROOT_FOLDER)

    def test_move_show_by_name(self):
        mover.move_episodes_by_name(
            'halt and catch fire',
            self.__SHOW_DESTINATION_ROOT_FOLDER,
            self.__SOURCE_DIRECTORY_PATH)

        destination_path = self.__SHOW_DESTINATION_ROOT_FOLDER + '/Halt And Catch Fire/Season 2/' + self.__TV_SHOW_FILE_NAME_1
        file_is_in_new_path = file_handler.check_file_existance(destination_path)
        self.assertTrue(file_is_in_new_path)

        source_path = self.__SOURCE_DIRECTORY_PATH + '/' + self.__TV_SHOW_FILE_NAME_1
        file_is_in_old_path = file_handler.check_file_existance(source_path)
        self.assertFalse(file_is_in_old_path)

    def test_move_show_by_file_path(self):
        source_file_path = self.__SOURCE_DIRECTORY_PATH + '/' + self.__TV_SHOW_FILE_NAME_2
        mover.move_media_by_path(source_file_path, self.__SHOW_DESTINATION_ROOT_FOLDER, self.__MOVIE_DESTINATION_ROOT_FOLDER)

        destination_path = self.__SHOW_DESTINATION_ROOT_FOLDER + '/The Last Man on Earth/Season 2/' + self.__TV_SHOW_FILE_NAME_2
        file_is_in_path = file_handler.check_file_existance(destination_path)
        self.assertTrue(file_is_in_path)

        file_is_in_old_path = file_handler.check_file_existance(source_file_path)
        self.assertFalse(file_is_in_old_path)

    def test_move_movie_by_file_path(self):
        source_file_path = self.__SOURCE_DIRECTORY_PATH + '/' + self.__MOVIE_FILE_NAME_1
        mover.move_media_by_path(source_file_path, self.__SHOW_DESTINATION_ROOT_FOLDER, self.__MOVIE_DESTINATION_ROOT_FOLDER)

        destination_path = self.__MOVIE_DESTINATION_ROOT_FOLDER + '/' + self.__MOVIE_FILE_NAME_1
        file_is_in_new_path = file_handler.check_file_existance(destination_path)
        self.assertTrue(file_is_in_new_path)

        file_is_in_old_path = file_handler.check_file_existance(source_file_path)
        self.assertFalse(file_is_in_old_path)
