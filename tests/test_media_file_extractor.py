import unittest

from episodeMover.media_file_extractor import MediaFileExtractor, Type, WrongMediatypeException


class MediaFileExtractorTest(unittest.TestCase):

    tv_shows_paths = [
        'testar/test/Falling.Skies.S02E03.720p.SOMETHING.SOMETHING-SOMETHING.mp4',
        'testar/intetest/The.Big.Bang.Theory.S09E01.something.something-something[something].mp4'
    ]

    movie_paths = [
        'testar/test/The.Great.Gatsby.2012.BluRay.1080p.DTS.x224-AAA.mkv'
    ]

    def test_type(self):
        media_file_extractor = MediaFileExtractor(self.tv_shows_paths[0])
        self.assertEqual(Type.TV_SHOW, media_file_extractor.get_type())

        media_file_extractor = MediaFileExtractor(self.movie_paths[0])
        self.assertEqual(Type.MOVIE, media_file_extractor.get_type())

        media_file_extractor = MediaFileExtractor(self.tv_shows_paths[1])
        self.assertEqual(Type.TV_SHOW, media_file_extractor.get_type())

    def test_extract_episode(self):
        media_file_extractor = MediaFileExtractor(self.tv_shows_paths[0])
        episode_number = media_file_extractor.get_episode_number()
        self.assertEqual('03', episode_number)

        media_file_extractor = MediaFileExtractor(self.tv_shows_paths[1])
        self.assertEqual('01', media_file_extractor.get_episode_number())

        media_file_extractor = MediaFileExtractor(self.movie_paths[0])
        self.assertRaises(WrongMediatypeException, media_file_extractor.get_episode_number)

    def text_extract_season(self):
        media_file_extractor = MediaFileExtractor(self.tv_shows_paths)
        season_number = media_file_extractor.get_season_number()
        self.assertEqual('09', season_number)

        season_number = media_file_extractor.get_season_number()
        self.assertEqual('02', season_number)

        media_file_extractor = MediaFileExtractor(self.tv_shows_paths)
        self.assertRaises(WrongMediatypeException, media_file_extractor.get_season_number())
