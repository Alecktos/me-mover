import subprocess
import unittest
import file_moved_assertion
from memover import file_handler


class AppTest(unittest.TestCase, file_moved_assertion.FileMovedAssertion):

    __SOURCE_DIRECTORY = 'sourcefolder'
    __SHOW_DESTINATION_DIRECTORY = 'show-destination'
    __MOVIE_DESTINATION_DIRECTORY = 'movie-destination'
    __TV_SHOW_FILE_NAME_1 = 'Con.with.fire.Fire.S02E10.720p.SOMETHING.something-SOMETHING.mkv'
    __TV_SHOW_FILE_NAME_2 = 'kolla.S04E15.asswe.xTTT-RR[abf].mkv'
    __TV_SHOW_FILE_NAME_3 = 'Con.with.fire.Fire.S01E01.720p.ANYTHING.ABJ.mkv'
    __MOVIE_FILE_NAME_1 = 'Fenix.Hart.And.Not.2001.DVDRip.DIVX.741-RO.mp4'
    __MOVIE_FILE_NAME_2 = 'ColdCraft (2016) FinSub CDROMRip x264 KORIG'

    __TV_SHOW_FILE_NAME_3_ORIGINAL = 'Old.Stuff.S02E15.720p.HDTV.x264-SVA[rarbg].cold'
    __TV_SHOW_FILE_NAME_3_PROPER = 'Old.Stuff.S02E15.PROPER.720p.HDTV.x264-KILLERS[rarbg].cold'

    __TV_SHOW_FILE_NAME_4 = 'Information Downloaded From www.akkero.com.txt'
    __TV_SHOW_FILE_NAME_4_PARENT_FOLDER = '[ www.gallero.it ] - Longer.S01E02.abg.AQS-A'

    def setUp(self):
        file_handler.create_dir(self.__SOURCE_DIRECTORY)
        file_handler.create_dir(self.__SHOW_DESTINATION_DIRECTORY)
        file_handler.create_dir(self.__MOVIE_DESTINATION_DIRECTORY)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_1)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_2)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_3)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_1)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_2)

        file_handler.create_dir(self.__SHOW_DESTINATION_DIRECTORY + '/Old Stuff/Season 2/')
        file_handler.create_file(self.__SHOW_DESTINATION_DIRECTORY + '/Old Stuff/Season 2/' + self.__TV_SHOW_FILE_NAME_3_ORIGINAL)
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_3_PROPER)

        parent_path = self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_4_PARENT_FOLDER
        file_handler.create_dir(parent_path)
        file_handler.create_file(parent_path + '/' + self.__TV_SHOW_FILE_NAME_4)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_DIRECTORY)
        file_handler.delete_directory(self.__SHOW_DESTINATION_DIRECTORY)
        file_handler.delete_directory(self.__MOVIE_DESTINATION_DIRECTORY)

    def test_moving_shows_with_wrong_formated_parent_folder(self):
        self.__run_app('file -file-path sourcefolder/[\ www.gallero.it\ ]\ -\ Longer.S01E02.abg.AQS-A/Information\ Downloaded\ From\ www.akkero.com.txt -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/Longer/Season 1/' + self.__TV_SHOW_FILE_NAME_4
        self.assertFileMoved(
            self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_4_PARENT_FOLDER + '/' + self.__TV_SHOW_FILE_NAME_4,
            destination_path
        )

    def test_moving_show_by_episode(self):
        """
        Undocumented but should be possible to move specific episode based by name, season and episode. Used internally
        """
        self.__run_app('name -name "con with fire fire S01E01" -source sourcefolder -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/Con with Fire Fire/Season 1/' + self.__TV_SHOW_FILE_NAME_3
        self.assertFileMoved(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_3, destination_path)

    def test_moving_show_by_name(self):
        self.__run_app('name -name "con with fire fire" -source sourcefolder -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/Con with Fire Fire/Season 2/' + self.__TV_SHOW_FILE_NAME_1
        self.assertFileMoved(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_1, destination_path)

    def test_moving_movie_by_name(self):
        self.__run_app('name -name "ColdCraft" -source sourcefolder -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__MOVIE_DESTINATION_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_2
        self.assertFileMoved(self.__SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_2, destination_path)

    def test_moving_movie_by_file(self):
        self.__run_app('file -file-path sourcefolder/Fenix.Hart.And.Not.2001.DVDRip.DIVX.741-RO.mp4 -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__MOVIE_DESTINATION_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_1
        self.assertFileMoved(self.__SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_1, destination_path)

    def test_moving_show_by_file(self):
        self.__run_app('file -file-path sourcefolder/kolla.S04E15.asswe.xTTT-RR[abf].mkv -show-destination show-destination -movie-destination movie-destination')
        destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/kolla/Season 4/' + self.__TV_SHOW_FILE_NAME_2
        self.assertFileMoved(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_2, destination_path)

    def test_that_proper_replace_old_episode(self):
        self.__run_app('file -file-path sourcefolder/Old.Stuff.S02E15.PROPER.720p.HDTV.x264-KILLERS[rarbg].cold -show-destination show-destination -movie-destination movie-destination')
        proper_file_destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/Old Stuff/Season 2/' + self.__TV_SHOW_FILE_NAME_3_PROPER
        wrong_file_destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/Old Stuff/Season 2/' + self.__TV_SHOW_FILE_NAME_3_ORIGINAL
        self.assertFalse(file_handler.check_file_existance(wrong_file_destination_path))
        self.assertFileMoved(self.__SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_3_PROPER, proper_file_destination_path)

    @staticmethod
    def __run_app(args):
        p = subprocess.Popen('python -m memover ' + args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line,

