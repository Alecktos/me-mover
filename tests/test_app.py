import subprocess
import unittest
import file_moved_assertion
from memover import file_handler


class AppTest(unittest.TestCase, file_moved_assertion.FileMovedAssertion):

    __SOURCE_DIRECTORY = 'sourcefolder'
    __SHOW_DESTINATION_DIRECTORY = 'show-destination'
    __MOVIE_DESTINATION_DIRECTORY = 'movie-destination'
    __TV_SHOW_FILE_NAME_1 = 'Halt.and.Catch.Fire.S02E10.720p.SOMETHING.something-SOMETHING.mkv'
    __TV_SHOW_FILE_NAME_2 = 'Vikings.S04E15.HDTV.xTTT-RR[abf].mkv'
    __MOVIE_FILE_NAME_1 = 'Kevin.Hart.What.Now.2016.DVDRip.DIVX.741-RO.mp4'
    __MOVIE_FILE_NAME_2 = 'Warcraft (2016) FinSub CDROMRip x264 KORIG'

    def setUp(self):
        file_handler.create_dir(self.__SOURCE_DIRECTORY)
        file_handler.create_dir(self.__SHOW_DESTINATION_DIRECTORY)
        file_handler.create_dir(self.__MOVIE_DESTINATION_DIRECTORY)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_1)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_2)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_1)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_2)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_DIRECTORY)
        file_handler.delete_directory(self.__SHOW_DESTINATION_DIRECTORY)
        file_handler.delete_directory(self.__MOVIE_DESTINATION_DIRECTORY)

    def test_moving_show_by_name(self):
        self.__run_app('name -name "halt and catch fire" -source sourcefolder -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/Halt And Catch Fire/Season 2/' + self.__TV_SHOW_FILE_NAME_1
        self.assertFileMoved(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_1, destination_path)

    def test_moving_movie_by_name(self):
        self.__run_app('name -name "Warcraft" -source sourcefolder -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__MOVIE_DESTINATION_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_2
        self.assertFileMoved(self.__SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_2, destination_path)

    def test_moving_movie_by_file(self):
        self.__run_app('file -file-path sourcefolder/Kevin.Hart.What.Now.2016.DVDRip.DIVX.741-RO.mp4 -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__MOVIE_DESTINATION_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_1
        self.assertFileMoved(self.__SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_1, destination_path)

    def test_moving_show_by_file(self):
        self.__run_app('file -file-path sourcefolder/Vikings.S04E15.HDTV.xTTT-RR[abf].mkv -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/Vikings/Season 4/' + self.__TV_SHOW_FILE_NAME_2
        self.assertFileMoved(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_2, destination_path)

    @staticmethod
    def __run_app(args):
        p = subprocess.Popen('python -m memover ' + args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line,

