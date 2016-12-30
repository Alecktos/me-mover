import unittest

from memover.media_file_extractor import MediaFileExtractor, Type, WrongMediatypeException


class MediaFileExtractorTest(unittest.TestCase):

    __TV_SHOWS_PATHS = [
        'testar/test/Falling.Skies.S02E03.720p.SOMETHING.SOMETHING-SOMETHING.mp4',
        'testar/intetest/The.Big.Bang.Theory.S09E01.something.something-something[something].mp4'
    ]

    __MOVIE_PATHS = [
        'testar/test/The.Great.Gatsby.2012.BluRay.1080p.DTS.x224-AAA.mkv'
    ]

    def test_type(self):
        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS[0])
        self.assertEqual(Type.TV_SHOW, media_file_extractor.get_type())

        media_file_extractor = MediaFileExtractor(self.__MOVIE_PATHS[0])
        self.assertEqual(Type.MOVIE, media_file_extractor.get_type())

        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS[1])
        self.assertEqual(Type.TV_SHOW, media_file_extractor.get_type())

    def test_extract_episode(self):
        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS[0])
        episode_number = media_file_extractor.get_episode_number()
        self.assertEqual('03', episode_number)

        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS[1])
        self.assertEqual('01', media_file_extractor.get_episode_number())

        media_file_extractor = MediaFileExtractor(self.__MOVIE_PATHS[0])
        self.assertRaises(WrongMediatypeException, media_file_extractor.get_episode_number)

    def text_extract_season(self):
        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS)
        season_number = media_file_extractor.get_season_number()
        self.assertEqual('09', season_number)

        season_number = media_file_extractor.get_season_number()
        self.assertEqual('02', season_number)

        media_file_extractor = MediaFileExtractor(self.__TV_SHOWS_PATHS)
        self.assertRaises(WrongMediatypeException, media_file_extractor.get_season_number())
