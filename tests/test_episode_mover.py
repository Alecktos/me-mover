import unittest
import file_moved_assertion
from memover import file_handler, episode_mover
from memover.media_file_extractor import MediaFileExtractor


class FileMoverTest(unittest.TestCase, file_moved_assertion.FileMovedAssertion):

    __SHOW_DESTINATION_PATH = 'show-destination'
    __SOURCE_PATH = 'source'

    __TV_SHOW_FILE_SOURCE_PATH = __SOURCE_PATH + '/aaa.bbb.s01e04.something.something-something.mp4'
    __TV_SHOW_FILE_DESTINATION_PATH = __SHOW_DESTINATION_PATH + '/aaa bbb/Season 1/aaa.bbb.s01e04.something.something-something.mp4'

    __TV_SHOW_2_FILE_1_SOURCE_PATH = __SOURCE_PATH + '/Moradeaa.S01E03.something.something-something.mkv'
    __TV_SHOW_2_FILE_1_DESTINATION_PATH = __SHOW_DESTINATION_PATH + '/Moradeaa/Season 1/Moradeaa.S01E03.something.something-something.mkv'

    __TV_SHOW_2_FILE_2_SOURCE_PATH = __SOURCE_PATH + '/Moradeaa.S01E02.something.something-something.mkv'
    __TV_SHOW_2_FILE_2_DESTINATION_PATH = __SHOW_DESTINATION_PATH + '/Moradeaa/Season 1/Moradeaa.S01E02.something.something-something.mkv'

    __TV_SHOW_2_FILE_3_ORIGINAL_2 = 'Mordeaa.S06E14.720p.HDTV.x000-Argos.mkv'
    __TV_SHOW_2_FILE_ORIGINAL_2_NFO = 'Mordeaa.S06E14.720p.HDTV.x000-Argos.nfo'
    __TV_SHOW_2_FILE_ORIGINAL_1 = 'Mordeaa.S06E15.720p.HDTV.x264-Sallad[rarbgag].mkv'
    __TV_SHOW_2_FILE_ORIGINAL_1_NFO = 'Mordeaa.S06E15.720p.HDTV.x264-Sallad[rarbgag].nfo'
    __TV_SHOW_2_FILE_PROPER = 'Mordeaa.S06E15.PROPER.720p.HDTV.x264-ARGON-[123].mkv'
    __TV_SHOW_2_FILE_PROPER_NFO = 'Mordeaa.S06E15.PROPER.720p.HDTV.x264-ARGON-[123].nfo'

    __TV_SHOW_3_SEASON_DESTINATION_DIRECTORY_PATH = __SHOW_DESTINATION_PATH + '/ABC/Season 9'
    __TV_SHOW_3_FILE_SOURCE_PATH = __SOURCE_PATH + '/abc.S09E02.something.something-something.mp4'
    __TV_SHOW_3_FILE_DESTINATION_PATH = __TV_SHOW_3_SEASON_DESTINATION_DIRECTORY_PATH + '/abc.S09E02.something.something-something.mp4'

    __TV_SHOW_4_DESTINATION_DIRECTORY_PATH = __SHOW_DESTINATION_PATH + '/Ab Cd Ef Gh/Season 10'
    __TV_SHOW_4_SOURCE_PATH = __SOURCE_PATH + '/Ab.Cd.Ef.Gh.PROPER.S10E13.720p.HDTV.q123-FLOOR.mkv'
    __TV_SHOW_4_DESTINATION_PATH = __TV_SHOW_4_DESTINATION_DIRECTORY_PATH + '/Ab.Cd.Ef.Gh.PROPER.S10E13.720p.HDTV.q123-FLOOR.mkv'

    __TV_SHOW_5_FILE_SOURCE_PATH = __SOURCE_PATH + '/Kongrass.2016.S01E06.720p.KONG-GG.maker.MAK.SWE.mkv'
    __TV_SHOW_5_DESTINATION_PATH = __SHOW_DESTINATION_PATH + '/Kongrass/Season 1/KOngrass.2016.S01E06.720p.KONG-GG.maker.MAK.SWE.mkv'

    __SAMPLE_FILE_SOURCE_DIRECTORY = __SOURCE_PATH + '/Felkod.S01E03.asd.dsa.dsa-AJKL[rarbg/Sample/'

    __SAMPLE_FILE_1_SOURCE_PATH = __SAMPLE_FILE_SOURCE_DIRECTORY + 'sample-felkod.s01e03.720p.ui.qq-oiu.mkv'
    __SAMPLE_FILE_1_DESTINATION_PATH = __SHOW_DESTINATION_PATH + '/felkod/Season 1/sample-felkod.s01e03.720p.ui.qq-oiu.mkv'

    __SAMPLE_FILE_2_SOURCE_PATH = __SAMPLE_FILE_SOURCE_DIRECTORY + 'sample.felkod.s01e03.720p.ui.qq-oiu.mkv'
    __SAMPLE_FILE_2_DESTINATION_PATH = __SHOW_DESTINATION_PATH + '/felkod/Season 1/sample.felkod.s01e03.720p.ui.qq-oiu.mkv'

    __SAMPLE_FILE_3_SOURCE_PATH = __SAMPLE_FILE_SOURCE_DIRECTORY + 'SaMple-felkod.s01e03.720p.aaa.x123-RORING.mkv'
    __SAMPLE_FILE_3_DESTINATION_PATH = __SHOW_DESTINATION_PATH + '/felkod/Season 1/SaMple-felkod.s01e03.720p.aaa.x123-RORING.mkv'

    def setUp(self):
        file_handler.create_dir(self.__SOURCE_PATH)

        file_handler.create_file(self.__TV_SHOW_2_FILE_1_SOURCE_PATH)
        file_handler.create_file(self.__TV_SHOW_FILE_SOURCE_PATH)
        file_handler.create_file(self.__TV_SHOW_2_FILE_2_SOURCE_PATH)
        file_handler.create_file(self.__TV_SHOW_3_FILE_SOURCE_PATH)
        file_handler.create_file(self.__TV_SHOW_4_SOURCE_PATH)

        file_handler.create_dir(self.__TV_SHOW_3_SEASON_DESTINATION_DIRECTORY_PATH)
        file_handler.create_dir(self.__TV_SHOW_4_DESTINATION_DIRECTORY_PATH)

        file_handler.create_dir(self.__SHOW_DESTINATION_PATH + '/Mordeaa/Season 6/')
        file_handler.create_file(self.__SHOW_DESTINATION_PATH + '/Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_1)
        file_handler.create_file(self.__SHOW_DESTINATION_PATH + '/Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_1_NFO)
        file_handler.create_file(self.__SHOW_DESTINATION_PATH + '/Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_3_ORIGINAL_2)
        file_handler.create_file(self.__SHOW_DESTINATION_PATH + '/Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_2_NFO)
        file_handler.create_file(self.__SOURCE_PATH + '/' + self.__TV_SHOW_2_FILE_PROPER)
        file_handler.create_file(self.__SOURCE_PATH + '/' + self.__TV_SHOW_2_FILE_PROPER_NFO)

        file_handler.create_dir(self.__SAMPLE_FILE_SOURCE_DIRECTORY)
        file_handler.create_file(self.__SAMPLE_FILE_1_SOURCE_PATH)
        file_handler.create_file(self.__SAMPLE_FILE_2_SOURCE_PATH)
        file_handler.create_file(self.__SAMPLE_FILE_3_SOURCE_PATH)

        file_handler.create_file(self.__TV_SHOW_5_FILE_SOURCE_PATH)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_PATH)
        file_handler.delete_directory(self.__SHOW_DESTINATION_PATH)

    def test_moving_files(self):
        self.__assert_moving_files([self.__TV_SHOW_2_FILE_1_SOURCE_PATH], [self.__TV_SHOW_2_FILE_1_DESTINATION_PATH])
        self.__assert_moving_files(
            [self.__TV_SHOW_FILE_SOURCE_PATH, self.__TV_SHOW_2_FILE_2_SOURCE_PATH],
            [self.__TV_SHOW_FILE_DESTINATION_PATH, self.__TV_SHOW_2_FILE_2_DESTINATION_PATH])

        self.__assert_moving_files(
            [self.__TV_SHOW_3_FILE_SOURCE_PATH],
            [self.__TV_SHOW_3_FILE_DESTINATION_PATH])  # test where season dir already exist

        self.__assert_moving_files(
            [self.__TV_SHOW_4_SOURCE_PATH],
            [self.__TV_SHOW_4_DESTINATION_PATH])  # test that we match against correct dist dir when the file is marked as PROPER

        self.__assert_moving_files(
            [self.__TV_SHOW_5_FILE_SOURCE_PATH],
            [self.__TV_SHOW_5_DESTINATION_PATH]
        )

        self.__assert_moving_files(
            [self.__SAMPLE_FILE_1_SOURCE_PATH, self.__SAMPLE_FILE_2_SOURCE_PATH, self.__SAMPLE_FILE_3_SOURCE_PATH],
            [self.__SAMPLE_FILE_1_DESTINATION_PATH, self.__SAMPLE_FILE_2_DESTINATION_PATH, self.__SAMPLE_FILE_3_DESTINATION_PATH]
        )

    def test_proper_episode_replaces_old(self):
        # moving media flle
        proper_file_source_path = self.__SOURCE_PATH + '/' + self.__TV_SHOW_2_FILE_PROPER
        proper_file_destination_path = self.__SHOW_DESTINATION_PATH + '/Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_PROPER

        # moving random file with same file name
        proper_file_source_path_nfo = self.__SOURCE_PATH + '/' + self.__TV_SHOW_2_FILE_PROPER_NFO
        proper_file_destination_path_nfo = self.__SHOW_DESTINATION_PATH + '/Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_PROPER_NFO

        self.__assert_moving_files(
            [proper_file_source_path, proper_file_source_path_nfo],
            [proper_file_destination_path, proper_file_destination_path_nfo]
        )

        # original 1 should not exist anymore
        original_1_path = self.__SHOW_DESTINATION_PATH + '/Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_1
        self.assertFalse(file_handler.check_file_existance(original_1_path))

        original_1_path = self.__SHOW_DESTINATION_PATH + '/Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_1_NFO
        self.assertFalse(file_handler.check_file_existance(original_1_path))

        # original 2 should still exist
        original_2_path = self.__SHOW_DESTINATION_PATH + '/Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_3_ORIGINAL_2
        self.assertTrue(file_handler.check_file_existance(original_2_path))

        original_2_path = self.__SHOW_DESTINATION_PATH + '/Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_2_NFO
        self.assertTrue(file_handler.check_file_existance(original_2_path))

    def __assert_moving_files(self, source_paths, destination_paths):
        # first loop and move everything
        for index, source_path in enumerate(source_paths):
            media_file_extractor = MediaFileExtractor(source_path)
            episode_mover.move_file(self.__SHOW_DESTINATION_PATH, media_file_extractor)

        # run assertions after moving
        for index, source_path in enumerate(source_paths):
            self.assertFileMoved(source_path, destination_paths[index])
