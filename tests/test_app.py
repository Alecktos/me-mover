import subprocess
import unittest
from memover import file_handler


class AppTest(unittest.TestCase):

    __SOURCE_DIRECTORY = 'sourcefolder'
    __SHOW_DESTINATION_DIRECTORY = 'show-destination'
    __MOVIE_DESTINATION_DIRECTORY = 'movie-destination'
    __TV_SHOW_FILE_NAME_1 = 'Halt.and.Catch.Fire.S02E10.720p.SOMETHING.something-SOMETHING.mkv'
    __TV_SHOW_FILE_NAME_2 = 'Vikings.S04E15.HDTV.x264-KILLERS[ettv].mkv'
    __MOVIE_FILE_NAME_1 = 'Kevin.Hart.What.Now.2016.DVDRip.XviD.AC3-EVO.mp4'

    def setUp(self):
        file_handler.create_dir(self.__SOURCE_DIRECTORY)
        file_handler.create_dir(self.__SHOW_DESTINATION_DIRECTORY)
        file_handler.create_dir(self.__MOVIE_DESTINATION_DIRECTORY)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_1)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_1)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_2)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_DIRECTORY)
        file_handler.delete_directory(self.__SHOW_DESTINATION_DIRECTORY)
        file_handler.delete_directory(self.__MOVIE_DESTINATION_DIRECTORY)

    def test_moving_show_by_name(self):
        self.__run_app('tvshow -show-name "halt and catch fire" -show-source sourcefolder -show-destination show-destination')
        destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/Halt And Catch Fire/Season 2/' + self.__TV_SHOW_FILE_NAME_1
        self.__assert_file_in_new_path(destination_path)
        self.__assert_file_not_in_old_path(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_1)

    def test_moving_movie_by_file(self):
        self.__run_app('file -file-path sourcefolder/Kevin.Hart.What.Now.2016.DVDRip.XviD.AC3-EVO.mp4 -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__MOVIE_DESTINATION_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_1
        self.__assert_file_in_new_path(destination_path)
        self.__assert_file_not_in_old_path(self.__SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_1)

    def test_moving_show_by_file(self):
        self.__run_app('file -file-path sourcefolder/Vikings.S04E15.HDTV.x264-KILLERS[ettv].mkv -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/Vikings/Season 4/' + self.__TV_SHOW_FILE_NAME_2
        self.__assert_file_in_new_path(destination_path)
        self.__assert_file_not_in_old_path(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_2)

    @staticmethod
    def __run_app(args):
        p = subprocess.Popen('python -m memover ' + args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line,

    def __assert_file_in_new_path(self, destination_path):
        file_is_in_new_path = file_handler.check_file_existance(destination_path)
        self.assertTrue(file_is_in_new_path)

    def __assert_file_not_in_old_path(self, source_path):
        file_is_in_old_path = file_handler.check_file_existance(source_path)
        self.assertFalse(file_is_in_old_path)
