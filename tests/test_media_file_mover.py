import unittest
from memover import mover, file_handler


class TestMediaFileMover(unittest.TestCase):

    __SOURCE_DIRECTORY_PATH = 'sourcefolder'
    __SHOW_DESTINATION_ROOT_FOLDER = 'destination_show'
    __MOVIE_DESTINATION_ROOT_FOLDER = 'destination_movie'
    __TV_SHOW_FILE_NAME = '/Halt.and.Catch.Fire.S02E10.720p.SOMETHING.something-SOMETHING.mkv'
    __TV_SHOW_FILE_SOURCE_PATH = __SOURCE_DIRECTORY_PATH + __TV_SHOW_FILE_NAME

    def setUp(self):
        file_handler.create_dir(self.__MOVIE_DESTINATION_ROOT_FOLDER)
        file_handler.create_dir(self.__SHOW_DESTINATION_ROOT_FOLDER)
        file_handler.create_dir(self.__SOURCE_DIRECTORY_PATH)
        file_handler.create_file(self.__TV_SHOW_FILE_SOURCE_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_DIRECTORY_PATH)
        file_handler.delete_directory(self.__SHOW_DESTINATION_ROOT_FOLDER)
        file_handler.delete_directory(self.__MOVIE_DESTINATION_ROOT_FOLDER)

    def test_move_movie(self):
        pass
        # destination_path = self.__SHOW_DESTINATION_ROOT_FOLDER + '/Halt and Catch Fire/Season 2' + self.__TV_SHOW_FILE_NAME
        #
        # mover.move_file(
        #     self.__TV_SHOW_FILE_SOURCE_PATH,
        #     self.__SHOW_DESTINATION_ROOT_FOLDER,
        #     self.__MOVIE_DESTINATION_ROOT_FOLDER)
        #
        # file_in_new_path = file_handler.check_file_existance(destination_path)
        # self.assertTrue(file_in_new_path)
