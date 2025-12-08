import unittest
from tests.utils import file_mover_tester
from memover import file_handler, episode_mover


class TestEpisodeMover(unittest.TestCase, file_mover_tester.FileMoverTester):

    def setUp(self):
        self._create_test_dirs()
        self.__TV_SHOW_FILE_SOURCE_PATH = 'aaa.bbb.s01e04.something.something-something.mp4'
        self.__TV_SHOW_FILE_DESTINATION_PATH = self._SHOW_DESTINATION_DIRECTORY + 'aaa bbb/Season 1/aaa.bbb.s01e04.something.something-something.mp4'

        self.__TV_SHOW_2_FILE_1_SOURCE_PATH = 'Moradeaa.S01E03.something.something-something.mkv'
        self.__TV_SHOW_2_FILE_1_DESTINATION_PATH = self._SHOW_DESTINATION_DIRECTORY + 'Moradeaa/Season 1/Moradeaa.S01E03.something.something-something.mkv'

        self.__TV_SHOW_2_FILE_2_SOURCE_PATH = 'Moradeaa.S01E02.something.something-something.mkv'
        self.__TV_SHOW_2_FILE_2_DESTINATION_PATH = self._SHOW_DESTINATION_DIRECTORY + 'Moradeaa/Season 1/Moradeaa.S01E02.something.something-something.mkv'

        self.__TV_SHOW_2_FILE_3_ORIGINAL_2 = 'Mordeaa.S06E14.720p.HDTV.x000-Argos.mkv'
        self.__TV_SHOW_2_FILE_ORIGINAL_2_NFO = 'Mordeaa.S06E14.720p.HDTV.x000-Argos.nfo'
        self.__TV_SHOW_2_FILE_ORIGINAL_1 = 'Mordeaa.S06E15.720p.HDTV.x264-Sallad[rarbgag].mkv'
        self.__TV_SHOW_2_FILE_ORIGINAL_1_NFO = 'Mordeaa.S06E15.720p.HDTV.x264-Sallad[rarbgag].nfo'
        self.__TV_SHOW_2_FILE_PROPER = 'Mordeaa.S06E15.PROPER.720p.HDTV.x264-ARGON-[123].mkv'
        self.__TV_SHOW_2_FILE_PROPER_NFO = 'Mordeaa.S06E15.PROPER.720p.HDTV.x264-ARGON-[123].nfo'

        self.__TV_SHOW_3_SEASON_DESTINATION_DIRECTORY_PATH = self._SHOW_DESTINATION_DIRECTORY + 'ABC/Season 9'
        self.__TV_SHOW_3_FILE_SOURCE_PATH = 'abc.S09E02.something.something-something.mp4'
        self.__TV_SHOW_3_FILE_DESTINATION_PATH = self.__TV_SHOW_3_SEASON_DESTINATION_DIRECTORY_PATH + '/abc.S09E02.something.something-something.mp4'

        self.__TV_SHOW_4_DESTINATION_DIRECTORY_PATH = self._SHOW_DESTINATION_DIRECTORY + 'Ab Cd Ef Gh/Season 10'
        self.__TV_SHOW_4_SOURCE_PATH = 'Ab.Cd.Ef.Gh.PROPER.S10E13.720p.HDTV.q123-FLOOR.mkv'
        self.__TV_SHOW_4_DESTINATION_PATH = self.__TV_SHOW_4_DESTINATION_DIRECTORY_PATH + '/Ab.Cd.Ef.Gh.PROPER.S10E13.720p.HDTV.q123-FLOOR.mkv'

        self.__TV_SHOW_5_FILE_SOURCE_PATH = 'Kongrass.2016.S01E06.720p.KONG-GG.maker.MAK.SWE.mkv'
        self.__TV_SHOW_5_DESTINATION_PATH = self._SHOW_DESTINATION_DIRECTORY + 'Kongrass/Season 1/Kongrass.2016.S01E06.720p.KONG-GG.maker.MAK.SWE.mkv'

        self.__SAMPLE_FILE_SOURCE_DIRECTORY = 'Felkod.S01E03.asd.dsa.dsa-AJKL[rarbg/Sample/'

        self.__SAMPLE_FILE_1_SOURCE_PATH = self.__SAMPLE_FILE_SOURCE_DIRECTORY + 'sample-felkod.s01e03.720p.ui.qq-oiu.mkv'
        self.__SAMPLE_FILE_1_DESTINATION_PATH = self._SHOW_DESTINATION_DIRECTORY + 'felkod/Season 1/sample-felkod.s01e03.720p.ui.qq-oiu.mkv'

        self.__SAMPLE_FILE_2_SOURCE_PATH = self.__SAMPLE_FILE_SOURCE_DIRECTORY + 'sample.felkod.s01e03.720p.ui.qq-oiu.mkv'
        self.__SAMPLE_FILE_2_DESTINATION_PATH = self._SHOW_DESTINATION_DIRECTORY + 'felkod/Season 1/sample.felkod.s01e03.720p.ui.qq-oiu.mkv'

        self.__SAMPLE_FILE_3_SOURCE_PATH = self.__SAMPLE_FILE_SOURCE_DIRECTORY + 'SaMple-felkod.s01e03.720p.aaa.x123-RORING.mkv'
        self.__SAMPLE_FILE_3_DESTINATION_PATH = self._SHOW_DESTINATION_DIRECTORY + 'felkod/Season 1/SaMple-felkod.s01e03.720p.aaa.x123-RORING.mkv'

        self._createSourceFile(self.__TV_SHOW_2_FILE_1_SOURCE_PATH)
        self._createSourceFile(self.__TV_SHOW_FILE_SOURCE_PATH)
        self._createSourceFile(self.__TV_SHOW_2_FILE_2_SOURCE_PATH)
        self._createSourceFile(self.__TV_SHOW_3_FILE_SOURCE_PATH)
        self._createSourceFile(self.__TV_SHOW_4_SOURCE_PATH)

        file_handler.create_dir(self.__TV_SHOW_3_SEASON_DESTINATION_DIRECTORY_PATH)
        file_handler.create_dir(self.__TV_SHOW_4_DESTINATION_DIRECTORY_PATH)

        file_handler.create_file(self._SHOW_DESTINATION_DIRECTORY + 'Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_1)
        file_handler.create_file(self._SHOW_DESTINATION_DIRECTORY + 'Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_1_NFO)
        file_handler.create_file(self._SHOW_DESTINATION_DIRECTORY + 'Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_3_ORIGINAL_2)
        file_handler.create_file(self._SHOW_DESTINATION_DIRECTORY + 'Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_2_NFO)
        self._createSourceFile(self.__TV_SHOW_2_FILE_PROPER)
        self._createSourceFile(self.__TV_SHOW_2_FILE_PROPER_NFO)

        self._createSourceFile(self.__SAMPLE_FILE_1_SOURCE_PATH)
        self._createSourceFile(self.__SAMPLE_FILE_2_SOURCE_PATH)
        self._createSourceFile(self.__SAMPLE_FILE_3_SOURCE_PATH)

        self._createSourceFile(self.__TV_SHOW_5_FILE_SOURCE_PATH)

    def tearDown(self):
        self._delete_test_dirs()

    def test_moving_files(self):
        self.__assert_tv_shows_files([self.__TV_SHOW_2_FILE_1_SOURCE_PATH], [self.__TV_SHOW_2_FILE_1_DESTINATION_PATH])
        self.__assert_tv_shows_files(
            [self.__TV_SHOW_FILE_SOURCE_PATH, self.__TV_SHOW_2_FILE_2_SOURCE_PATH],
            [self.__TV_SHOW_FILE_DESTINATION_PATH, self.__TV_SHOW_2_FILE_2_DESTINATION_PATH])

        # test where season dir already exist
        self.__assert_tv_shows_files(
            [self.__TV_SHOW_3_FILE_SOURCE_PATH],
            [self.__TV_SHOW_3_FILE_DESTINATION_PATH])

        # test that we match against correct dist dir when the file is marked as PROPER
        self.__assert_tv_shows_files(
            [self.__TV_SHOW_4_SOURCE_PATH],
            [self.__TV_SHOW_4_DESTINATION_PATH])

        self.__assert_tv_shows_files(
            [self.__TV_SHOW_5_FILE_SOURCE_PATH],
            [self.__TV_SHOW_5_DESTINATION_PATH]
        )

        self.__assert_tv_shows_files(
            [self.__SAMPLE_FILE_1_SOURCE_PATH, self.__SAMPLE_FILE_2_SOURCE_PATH, self.__SAMPLE_FILE_3_SOURCE_PATH],
            [self.__SAMPLE_FILE_1_DESTINATION_PATH, self.__SAMPLE_FILE_2_DESTINATION_PATH, self.__SAMPLE_FILE_3_DESTINATION_PATH]
        )

    def test_proper_episode_replaces_old(self):
        # moving media flle
        proper_file_source_path = self.__TV_SHOW_2_FILE_PROPER
        proper_file_destination_path = self._SHOW_DESTINATION_DIRECTORY + 'Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_PROPER

        # moving random file with same file name
        proper_file_source_path_nfo = self.__TV_SHOW_2_FILE_PROPER_NFO
        proper_file_destination_path_nfo = self._SHOW_DESTINATION_DIRECTORY + 'Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_PROPER_NFO

        self.__assert_tv_shows_files(
            [proper_file_source_path, proper_file_source_path_nfo],
            [proper_file_destination_path, proper_file_destination_path_nfo]
        )

        # original 1 should not exist anymore
        original_1_path = self._SHOW_DESTINATION_DIRECTORY + 'Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_1
        self.assertFalse(file_handler.file_exist(original_1_path))

        original_1_path = self._SHOW_DESTINATION_DIRECTORY + 'Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_1_NFO
        self.assertFalse(file_handler.file_exist(original_1_path))

        # original 2 should still exist
        original_2_path = self._SHOW_DESTINATION_DIRECTORY + 'Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_3_ORIGINAL_2
        self.assertTrue(file_handler.file_exist(original_2_path))

        original_2_path = self._SHOW_DESTINATION_DIRECTORY + 'Mordeaa/Season 6/' + self.__TV_SHOW_2_FILE_ORIGINAL_2_NFO
        self.assertTrue(file_handler.file_exist(original_2_path))

    def __assert_tv_shows_files(self, source_paths, destination_paths):
        # first loop and move everything
        for index, source_path in enumerate(source_paths):
            episode_mover.move(self._SHOW_DESTINATION_DIRECTORY, self._SOURCE_DIRECTORY + source_path)

        # run assertions after moving
        for index, source_path in enumerate(source_paths):
            self._assert_file_moved(source_path, destination_paths[index])
