import unittest
from tests.utils import file_mover_tester

from memover.media_file_extractor import get_type, Type, WrongMediaTypeException, EpisodeFile


class TestMediaFileExtractor(unittest.TestCase, file_mover_tester.FileMoverTester):

    __TV_SHOWS_PATHS = [
        'testar/test/Another.Another.S02E03.720p.SOMETHING.SOMETHING-SOMETHING.mp4',
        'testar/intetest/Other.Other.Other.Other.S09E01.something.something-something[something].mp4',
        'testar/[ www.flobbing.com ] - Longer.S01E02.HaHV.Maam-A/Information Downloaded From www.akkero.com.txt',
        'testar/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig/Stuff from www.Lobertar.com.mkv'
    ]

    __MOVIE_PATHS = [
        'testar/test/Greater.Great.Greatest.2009.StenRay.123p.DTS.2224-AAA.mkv'
    ]

    def setUp(self):
        self._create_test_dirs()
        for path in self.__TV_SHOWS_PATHS:
            self._createSourceFile(path)

        for path in self.__MOVIE_PATHS:
            self._createSourceFile(path)

    def tearDown(self):
        self._delete_test_dirs()

    def test_type(self):
        self.assertEqual(Type.TV_SHOW, get_type(self._SOURCE_DIRECTORY + self.__TV_SHOWS_PATHS[0]))

        self.assertEqual(Type.MOVIE, get_type(self._SOURCE_DIRECTORY + self.__MOVIE_PATHS[0]))

        self.assertEqual(Type.TV_SHOW, get_type(self._SOURCE_DIRECTORY + self.__TV_SHOWS_PATHS[1]))

    def test_extract_episode(self):
        media_file_extractor = EpisodeFile(self.__TV_SHOWS_PATHS[0])
        episode_number = media_file_extractor.get_episode_number()
        self.assertEqual('03', episode_number)

        media_file_extractor = EpisodeFile(self.__TV_SHOWS_PATHS[1])
        self.assertEqual('01', media_file_extractor.get_episode_number())

        # self.assertRaises(Exception, MyClass, foo)
        self.assertRaises(WrongMediaTypeException, EpisodeFile, self.__MOVIE_PATHS[0])

    def test_extract_season(self):
        media_file_extractor = EpisodeFile(self.__TV_SHOWS_PATHS[0])
        season_number = media_file_extractor.get_season()
        self.assertEqual('02', season_number)

        media_file_extractor = EpisodeFile(self.__TV_SHOWS_PATHS[1])
        season_number = media_file_extractor.get_season()
        self.assertEqual('09', season_number)

    def test_extract_show_name(self):
        media_file_extractor = EpisodeFile(self.__TV_SHOWS_PATHS[2])
        show_name = media_file_extractor.get_tv_show_name()
        self.assertEqual('Longer', show_name)

    def test_extract_urls(self):
        media_file_extractor = EpisodeFile(self.__TV_SHOWS_PATHS[3])
        show_name = media_file_extractor.get_tv_show_name()
        self.assertEqual('Long', show_name)
