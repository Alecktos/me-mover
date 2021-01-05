import unittest

from memover import media_file_extractor
from memover.media_file_extractor import Type
from tests.utils import file_mover_tester


class TestMediaFileExtractor(unittest.TestCase, file_mover_tester.FileMoverTester):

    __TV_SHOWS_PATHS = [
        'testar/test/Another.Another.S02E03.720p.SOMETHING.SOMETHING-SOMETHING.mp4',
        'testar/intetest/Other.Other.Other.Other.S09E01.something.something-something[something].mp4',
        'testar/[ www.flobbing.com ] - Longer.S01E02.HaHV.Maam-A/Information Downloaded From www.akkero.com.txt',
        'testar/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig/Stuff from www.Lobertar.com.mkv',
        'title/title - Title.S01E02.720p.KOOK.asdf-Risig.mkv',
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
        self.assertEqual(Type.TV_SHOW, media_file_extractor.get_type(self._SOURCE_DIRECTORY + self.__TV_SHOWS_PATHS[0]))

        self.assertEqual(Type.MOVIE, media_file_extractor.get_type(self._SOURCE_DIRECTORY + self.__MOVIE_PATHS[0]))

        self.assertEqual(Type.TV_SHOW, media_file_extractor.get_type(self._SOURCE_DIRECTORY + self.__TV_SHOWS_PATHS[1]))

    def test_extract_episode(self):
        episode_number = media_file_extractor.get_episode_number(self.__TV_SHOWS_PATHS[0])
        self.assertEqual('03', episode_number)

        self.assertEqual('01', media_file_extractor.get_episode_number(self.__TV_SHOWS_PATHS[1]))

        self.assertRaises(media_file_extractor.WrongMediaTypeException, media_file_extractor.get_season, self.__MOVIE_PATHS[0])

    def test_extract_show_name(self):
        show_name = media_file_extractor.get_tv_show_name(self.__TV_SHOWS_PATHS[2])
        self.assertEqual('Longer', show_name)

    def test_remove_urls_show_name(self):
        show_name = media_file_extractor.get_tv_show_name(self.__TV_SHOWS_PATHS[3])
        self.assertEqual('Long', show_name)

    def test_no_valid_show_name(self):
        self.assertRaises(
            media_file_extractor.CouldNotExtractShowNameException,
            media_file_extractor.get_tv_show_name,
            self.__TV_SHOWS_PATHS[4]
        )

    def test_extract_season(self):
        season_number = media_file_extractor.get_season(self.__TV_SHOWS_PATHS[0])
        self.assertEqual('02', season_number)

        season_number = media_file_extractor.get_season(self.__TV_SHOWS_PATHS[1])
        self.assertEqual('09', season_number)
