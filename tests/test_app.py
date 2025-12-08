import subprocess
import sys
import unittest
from tests.utils import file_mover_tester
from memover import file_handler


class TestApp(unittest.TestCase, file_mover_tester.FileMoverTester):

    __TV_SHOW_FILE_NAME_1 = 'Con.with.fire.Fire.S02E10.720p.SOMETHING.something-SOMETHING.mkv'
    __TV_SHOW_FILE_NAME_2 = 'kolla.S04E15.asswe.xTTT-RR[abf].mkv'
    __TV_SHOW_FILE_NAME_3 = 'Con.with.fire.Fire.S01E01.720p.ANYTHING.ABJ.mkv'
    __MOVIE_FILE_NAME_1 = 'Fenix.Hart.And.Not.2001.DVDRip.DIVX.741-RO.mp4'
    __MOVIE_FILE_NAME_2 = 'ColdCraft (2016) FinSub CDROMRip x264 KORIG'

    __TV_SHOW_FILE_NAME_3_ORIGINAL = 'Old.Stuff.S02E15.720p.HDTV.x264-SVA[rarbg].cold'
    __TV_SHOW_FILE_NAME_3_PROPER = 'Old.Stuff.S02E15.PROPER.720p.HDTV.x264-KILLERS[rarbg].cold'

    __TV_SHOW_FILE_NAME_4 = 'Information Downloaded From www.akkero.com.txt'
    __TV_SHOW_FILE_NAME_4_PARENT_FOLDER = '[ www.gallero.it ] - Longer.S01E02.abg.AQS-A'

    __TV_SHOW_FILE_NAME_5 = 'Stuff from www.Lobertar.com.mkv'
    __TV_SHOW_FILE_NAME_5_PARENT_FOLDER = 'www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig'

    def setUp(self):
        self._create_test_dirs()
        file_handler.create_file(self._SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_1)
        file_handler.create_file(self._SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_2)
        file_handler.create_file(self._SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_3)
        file_handler.create_file(self._SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_1)
        file_handler.create_file(self._SOURCE_DIRECTORY + '/' + self.__MOVIE_FILE_NAME_2)

        file_handler.create_dir(self._SHOW_DESTINATION_DIRECTORY + 'Old Stuff/Season 2/')
        file_handler.create_file(self._SHOW_DESTINATION_DIRECTORY + 'Old Stuff/Season 2/' + self.__TV_SHOW_FILE_NAME_3_ORIGINAL)
        file_handler.create_file(self._SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_3_PROPER)

        parent_path = self._SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_4_PARENT_FOLDER
        file_handler.create_dir(parent_path)
        file_handler.create_file(parent_path + '/' + self.__TV_SHOW_FILE_NAME_4)

        parent_path = self._SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_5_PARENT_FOLDER
        file_handler.create_dir(parent_path)
        file_handler.create_file(parent_path + '/' + self.__TV_SHOW_FILE_NAME_5)

    def tearDown(self):
        self._delete_test_dirs()

    def test_moving_shows_with_wrong_formated_parent_folder(self):
        self.__run_by_file(r'sourcefolder/[\ www.gallero.it\ ]\ -\ Longer.S01E02.abg.AQS-A/Information\ Downloaded\ From\ www.akkero.com.txt')
        destination_path = self._SHOW_DESTINATION_DIRECTORY + 'Longer/Season 1/' + self.__TV_SHOW_FILE_NAME_4
        self._assert_file_moved(
            self._SOURCE_DIRECTORY + self.__TV_SHOW_FILE_NAME_4_PARENT_FOLDER + '/' + self.__TV_SHOW_FILE_NAME_4,
            destination_path
        )

    def test_moving_show_with_urls(self):
        self.__run_by_file(r'sourcefolder/www.Lobertar.com\ -\ Long.S01E02.720p.KOOK.asdf-Risig/Stuff\ from\ www.Lobertar.com.mkv')
        destination_path = self._SHOW_DESTINATION_DIRECTORY + 'Long/Season 1/' + self.__TV_SHOW_FILE_NAME_5
        self._assert_file_moved(
            self._SOURCE_DIRECTORY + self.__TV_SHOW_FILE_NAME_5_PARENT_FOLDER + '/' + self.__TV_SHOW_FILE_NAME_5,
            destination_path
        )

    def test_moving_show_by_episode(self):
        """
        Undocumented but should be possible to move specific episode based by name, season and episode. Used internally
        """
        self.__run_by_name('con with fire fire S01E01')
        destination_path = self._SHOW_DESTINATION_DIRECTORY + 'Con with fire Fire/Season 1/' + self.__TV_SHOW_FILE_NAME_3
        self._assert_file_moved(self._SOURCE_DIRECTORY + '/' + self.__TV_SHOW_FILE_NAME_3, destination_path)

    def test_moving_show_by_name(self):
        self.__run_by_name('con with fire fire')
        destination_path = self._SHOW_DESTINATION_DIRECTORY + 'Con with fire Fire/Season 2/' + self.__TV_SHOW_FILE_NAME_1
        self._assert_file_moved(self._SOURCE_DIRECTORY + self.__TV_SHOW_FILE_NAME_1, destination_path)

    def test_moving_movie_by_name(self):
        self.__run_by_name('ColdCraft')
        destination_path = self._MOVIE_DESTINATION_DIRECTORY + self.__MOVIE_FILE_NAME_2 + '/' + self.__MOVIE_FILE_NAME_2
        self._assert_file_moved(self._SOURCE_DIRECTORY + self.__MOVIE_FILE_NAME_2, destination_path)

    def test_moving_movie_by_file(self):
        self.__run_by_file('sourcefolder/Fenix.Hart.And.Not.2001.DVDRip.DIVX.741-RO.mp4')
        destination_path = self._MOVIE_DESTINATION_DIRECTORY + '/Fenix.Hart.And.Not.2001.DVDRip.DIVX.741-RO/' + self.__MOVIE_FILE_NAME_1
        self._assert_file_moved(self._SOURCE_DIRECTORY + self.__MOVIE_FILE_NAME_1, destination_path)

    def test_moving_show_by_file(self):
        self.__run_by_file('sourcefolder/kolla.S04E15.asswe.xTTT-RR[abf].mkv')
        destination_path = self._SHOW_DESTINATION_DIRECTORY + 'kolla/Season 4/' + self.__TV_SHOW_FILE_NAME_2
        self._assert_file_moved(self._SOURCE_DIRECTORY + self.__TV_SHOW_FILE_NAME_2, destination_path)

    def test_that_proper_replace_old_episode(self):
        self.__run_by_file('sourcefolder/Old.Stuff.S02E15.PROPER.720p.HDTV.x264-KILLERS[rarbg].cold')
        proper_file_destination_path = self._SHOW_DESTINATION_DIRECTORY + 'Old Stuff/Season 2/' + self.__TV_SHOW_FILE_NAME_3_PROPER
        wrong_file_destination_path = self._SHOW_DESTINATION_DIRECTORY + 'Old Stuff/Season 2/' + self.__TV_SHOW_FILE_NAME_3_ORIGINAL
        self.assertFalse(file_handler.file_exist(wrong_file_destination_path))
        self._assert_file_moved(self._SOURCE_DIRECTORY + self.__TV_SHOW_FILE_NAME_3_PROPER, proper_file_destination_path)

    def test_moving_file_by_parent(self):
        source_dir = self._SOURCE_DIRECTORY + self.__TV_SHOW_FILE_NAME_4_PARENT_FOLDER + '/'
        self.__run_by_file(r'sourcefolder/[\ www.gallero.it\ ]\ -\ Longer.S01E02.abg.AQS-A')
        self._assert_file_moved(source_dir, self._SHOW_DESTINATION_DIRECTORY + 'Longer/Season 1/' + self.__TV_SHOW_FILE_NAME_4)

    @staticmethod
    def __run_by_name(show_name):
        TestApp.__run_app(f'by-name "{show_name}" sourcefolder show-destination movie-destination')

    @staticmethod
    def __run_by_file(source_file_path):
        TestApp.__run_app(f'by-path {source_file_path} show-destination movie-destination')

    @staticmethod
    def __run_app(args):
        with subprocess.Popen(
                f'{sys.executable} -m memover {args}',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
        ) as p:
            for line in p.stdout:
                print(line)
            p.wait()
