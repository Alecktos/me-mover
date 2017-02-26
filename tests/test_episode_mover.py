import unittest
import file_moved_assertion
from memover import file_handler, episode_mover
from memover.media_file_extractor import MediaFileExtractor


class FileMoverTest(unittest.TestCase, file_moved_assertion.FileMovedAssertion):

    __SHOW_DESTINATION_PATH = 'show-destination'
    __SOURCE_PATH = 'source'

    __NEW_GIRL_FILE_SOURCE_PATH = __SOURCE_PATH + '/new.girl.s01e04.something.something-something.mp4'
    __NEW_GIRL_FILE_DESTINATION_PATH = __SHOW_DESTINATION_PATH + '/new girl/Season 1/new.girl.s01e04.something.something-something.mp4'

    __HEROES_FILE_1_SOURCE_PATH = __SOURCE_PATH + '/HEROES.S01E03.something.something-something.mkv'
    __HEROES_FILE_1_DESTINATION_PATH = __SHOW_DESTINATION_PATH + '/Heroes/Season 1/HEROES.S01E03.something.something-something.mkv'

    __HEROES_FILE_2_SOURCE_PATH = __SOURCE_PATH + '/HEROES.S01E02.something.something-something.mkv'
    __HEROES_FILE_2_DESTINATION_PATH = __SHOW_DESTINATION_PATH + '/Heroes/Season 1/HEROES.S01E02.something.something-something.mkv'

    __ABC_SEASON_DESTINATION_DIRECTORY_PATH = __SHOW_DESTINATION_PATH + '/ABC/Season 9'
    __ABC_FILE_SOURCE_PATH = __SOURCE_PATH + '/abc.S09E02.something.something-something.mp4'
    __ABC_FILE_DESTINATION_PATH = __ABC_SEASON_DESTINATION_DIRECTORY_PATH + '/abc.S09E02.something.something-something.mp4'

    __BIG_BANG_THEORY_DESTINATION_DIRECTORY_PATH = __SHOW_DESTINATION_PATH + '/The Big Bang Theory/Season 10'
    __BIG_BANG_THEORY_SOURCE_PATH = __SOURCE_PATH + '/The.Big.Bang.Theory.PROPER.S10E13.720p.HDTV.q123-FLOOR.mkv'
    __BIG_BANG_THEORY_DESTINATION_PATH = __BIG_BANG_THEORY_DESTINATION_DIRECTORY_PATH + '/The.Big.Bang.Theory.PROPER.S10E13.720p.HDTV.q123-FLOOR.mkv'

    __NEW_GIRL_FILE_ORIGINAL_2 = 'New.Girl.S06E14.720p.HDTV.x264-FLEET.mkv'
    __NEW_GIRL_FILE_ORIGINAL_1 = 'New.Girl.S06E15.720p.HDTV.x264-SVA[rarbg].mkv'
    __NEW_GIRL_FILE_PROPER = 'New.Girl.S06E15.PROPER.720p.HDTV.x264-KILLERS[rarbg].mkv'

    __TIMELESS_FILE_SOURCE_PATH = __SOURCE_PATH + '/Timeless.2016.S01E06.720p.KONG-GG.maker.MAK.SWE.mkv'
    __TIMELESS_FILE_DESTINATION_PATH = __SHOW_DESTINATION_PATH + '/Timeless/Season 1/Timeless.2016.S01E06.720p.KONG-GG.maker.MAK.SWE.mkv'

    def setUp(self):
        file_handler.create_dir(self.__SOURCE_PATH)

        file_handler.create_file(self.__HEROES_FILE_1_SOURCE_PATH)
        file_handler.create_file(self.__NEW_GIRL_FILE_SOURCE_PATH)
        file_handler.create_file(self.__HEROES_FILE_2_SOURCE_PATH)
        file_handler.create_file(self.__ABC_FILE_SOURCE_PATH)
        file_handler.create_file(self.__BIG_BANG_THEORY_SOURCE_PATH)

        file_handler.create_dir(self.__ABC_SEASON_DESTINATION_DIRECTORY_PATH)
        file_handler.create_dir(self.__BIG_BANG_THEORY_DESTINATION_DIRECTORY_PATH)

        file_handler.create_dir(self.__SHOW_DESTINATION_PATH + '/New Girl/Season 6/')
        file_handler.create_file(self.__SHOW_DESTINATION_PATH + '/New Girl/Season 6/' + self.__NEW_GIRL_FILE_ORIGINAL_1)
        file_handler.create_file(self.__SHOW_DESTINATION_PATH + '/New Girl/Season 6/' + self.__NEW_GIRL_FILE_ORIGINAL_2)
        file_handler.create_file(self.__SOURCE_PATH + '/' + self.__NEW_GIRL_FILE_PROPER)

        file_handler.create_file(self.__TIMELESS_FILE_SOURCE_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_PATH)
        file_handler.delete_directory(self.__SHOW_DESTINATION_PATH)

    def test_moving_files(self):
        self.__assert_moving_files([self.__HEROES_FILE_1_SOURCE_PATH], [self.__HEROES_FILE_1_DESTINATION_PATH])
        self.__assert_moving_files(
            [self.__NEW_GIRL_FILE_SOURCE_PATH, self.__HEROES_FILE_2_SOURCE_PATH],
            [self.__NEW_GIRL_FILE_DESTINATION_PATH, self.__HEROES_FILE_2_DESTINATION_PATH])

        self.__assert_moving_files(
            [self.__ABC_FILE_SOURCE_PATH],
            [self.__ABC_FILE_DESTINATION_PATH])  # test where season dir already exist

        self.__assert_moving_files(
            [self.__BIG_BANG_THEORY_SOURCE_PATH],
            [self.__BIG_BANG_THEORY_DESTINATION_PATH])  # test that we match against correct dist dir when the file is marked as PROPER

        self.__assert_moving_files(
            [self.__TIMELESS_FILE_SOURCE_PATH],
            [self.__TIMELESS_FILE_DESTINATION_PATH]
        )

    def test_proper_episode_replaces_old(self):
        proper_file_source_path = self.__SOURCE_PATH + '/' + self.__NEW_GIRL_FILE_PROPER
        proper_file_destination_path = self.__SHOW_DESTINATION_PATH + '/New Girl/Season 6/' + self.__NEW_GIRL_FILE_PROPER
        self.__assert_moving_files([proper_file_source_path], [proper_file_destination_path])

        # original 1 should not exist anymore
        original_1_path = self.__SHOW_DESTINATION_PATH + '/New Girl/Season 6/' + self.__NEW_GIRL_FILE_ORIGINAL_1
        self.assertFalse(file_handler.check_file_existance(original_1_path))

        # original 2 should still exist
        original_2_path = self.__SHOW_DESTINATION_PATH + '/New Girl/Season 6/' + self.__NEW_GIRL_FILE_ORIGINAL_2
        self.assertTrue(file_handler.check_file_existance(original_2_path))

    def __assert_moving_files(self, source_paths, destination_paths):
        for index, source_path in enumerate(source_paths):
            media_file_extractor = MediaFileExtractor(source_path)
            episode_mover.move_file(self.__SHOW_DESTINATION_PATH, media_file_extractor)
            self.assertFileMoved(source_path, destination_paths[index])
