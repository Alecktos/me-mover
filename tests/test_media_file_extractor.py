import unittest

from memover.media_file_extractor import MediaFileExtractor, Type, WrongMediaTypeException


class MediaFileExtractorTest(unittest.TestCase):

    __TV_SHOWS_PATHS = [
        'testar/test/Another.Another.S02E03.720p.SOMETHING.SOMETHING-SOMETHING.mp4',
        'testar/intetest/Other.Other.Other.Other.S09E01.something.something-something[something].mp4'
    ]

    __MOVIE_PATHS = [
        'testar/test/Greater.Great.Greatest.2009.StenRay.123p.DTS.2224-AAA.mkv'
    ]

    def test_type(self):
        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS[0])
        self.assertEqual(Type.TV_SHOW, media_file_extractor.get_media_type())

        media_file_extractor = MediaFileExtractor(self.__MOVIE_PATHS[0])
        self.assertEqual(Type.MOVIE, media_file_extractor.get_media_type())

        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS[1])
        self.assertEqual(Type.TV_SHOW, media_file_extractor.get_media_type())

    def test_extract_episode(self):
        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS[0])
        episode_number = media_file_extractor.get_episode_number()
        self.assertEqual('03', episode_number)

        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS[1])
        self.assertEqual('01', media_file_extractor.get_episode_number())

        media_file_extractor = MediaFileExtractor(self.__MOVIE_PATHS[0])
        self.assertRaises(WrongMediaTypeException, media_file_extractor.get_episode_number)

    def text_extract_season(self):
        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS)
        season_number = media_file_extractor.get_season_number()
        self.assertEqual('09', season_number)

        season_number = media_file_extractor.get_season_number()
        self.assertEqual('02', season_number)

        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS)
        self.assertRaises(WrongMediaTypeException, media_file_extractor.get_season_number())
