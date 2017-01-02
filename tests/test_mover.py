import unittest
import file_moved_assertion
from memover import file_handler, mover


class MoverTest(unittest.TestCase, file_moved_assertion.FileMovedAssertion):

    __SOURCE_DIRECTORY = 'sourcefolder'
    __SHOW_DESTINATION_DIRECTORY = 'destination_show'
    __MOVIE_DESTINATION_DIRECTORY = 'destination_movie'

    def setUp(self):
        file_handler.create_dir(self.__MOVIE_DESTINATION_DIRECTORY)
        file_handler.create_dir(self.__SHOW_DESTINATION_DIRECTORY)
        file_handler.create_dir(self.__SHOW_DESTINATION_DIRECTORY + '/Shameless/Season 7/')
        file_handler.create_dir(self.__SOURCE_DIRECTORY)

    def tearDown(self):
        file_handler.delete_directory(self.__SOURCE_DIRECTORY)
        file_handler.delete_directory('destination_show')
        file_handler.delete_directory(self.__MOVIE_DESTINATION_DIRECTORY)

    def test_move_show_by_name(self):
        tv_show_file_name = 'Halt.and.Catch.Fire.S02E10.720p.SOMETHING.something-SOMETHING.mkv'
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + tv_show_file_name)

        mover.move_media_by_name(
            'halt and catch fire',
            self.__SOURCE_DIRECTORY,
            self.__SHOW_DESTINATION_DIRECTORY,
            self.__MOVIE_DESTINATION_DIRECTORY
        )

        destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/Halt And Catch Fire/Season 2/' + tv_show_file_name
        file_is_in_new_path = file_handler.check_file_existance(destination_path)
        self.assertTrue(file_is_in_new_path)

        source_path = self.__SOURCE_DIRECTORY + '/' + tv_show_file_name
        file_is_in_old_path = file_handler.check_file_existance(source_path)
        self.assertFalse(file_is_in_old_path)

    def test_move_show_by_file_path(self):
        tv_show_file_name = 'The.Last.Man.on.Earth.S02E03.Dead.Man.Walking.720p.WEB-DL.x123.BBA.mp4'
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + tv_show_file_name)

        source_file_path = self.__SOURCE_DIRECTORY + '/' + tv_show_file_name
        mover.move_media_by_path(source_file_path, self.__SHOW_DESTINATION_DIRECTORY, self.__MOVIE_DESTINATION_DIRECTORY)

        destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/The Last Man on Earth/Season 2/' + tv_show_file_name
        self.assertFileMoved(source_file_path, destination_path)

    def test_move_movie_by_file_path(self):
        movie_file_name = 'Fantastic Beast and Where To Find Them 2016 HD-TS x264-CPG.mkv'
        file_handler.create_file(self.__SOURCE_DIRECTORY + '/' + movie_file_name)

        source_file_path = self.__SOURCE_DIRECTORY + '/' + movie_file_name
        mover.move_media_by_path(source_file_path, self.__SHOW_DESTINATION_DIRECTORY, self.__MOVIE_DESTINATION_DIRECTORY)

        destination_path = self.__MOVIE_DESTINATION_DIRECTORY + '/' + movie_file_name
        self.assertFileMoved(source_file_path, destination_path)

    def test_move_show_into_existing_season_directory(self):
        tv_show_file_name = 'Shameless.US.S07E02.720p.HDTV.X264-DIMENSION[rarbg]'
        file_source_path = self.__SOURCE_DIRECTORY + '/' + tv_show_file_name
        file_handler.create_file(file_source_path)

        # move by name
        mover.move_media_by_name(
            'Shameless',
            self.__SOURCE_DIRECTORY,
            self.__SHOW_DESTINATION_DIRECTORY,
            self.__MOVIE_DESTINATION_DIRECTORY
        )

        file_destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/Shameless/Season 7/' + tv_show_file_name
        self.assertFileMoved(file_source_path, file_destination_path)

        # move by file
        file_handler.delete_file(file_destination_path)
        file_handler.create_file(file_source_path)
        mover.move_media_by_path(file_source_path, self.__SHOW_DESTINATION_DIRECTORY, self.__MOVIE_DESTINATION_DIRECTORY)
        self.assertFileMoved(file_source_path, file_destination_path)

    def test_moving_episodes_by_file_in_directory(self):
        folder_path = self.__SOURCE_DIRECTORY + '/hey.arnold.season1.720p.webdl'
        file_handler.create_dir(folder_path)
        source_file_path_1 = folder_path + '/hey.arnold.S09E01.SOMETHING.something-something'
        file_handler.create_file(source_file_path_1)

        source_file_path_2 = folder_path + '/hey.arnold.S09E02.SOMETHING.something-something.mp4'
        file_handler.create_file(source_file_path_2)

        mover.move_media_by_path(folder_path, self.__SHOW_DESTINATION_DIRECTORY, self.__MOVIE_DESTINATION_DIRECTORY)

        file_destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/hey arnold/Season 9/hey.arnold.S09E01.SOMETHING.something-something'
        self.assertFileMoved(source_file_path_1, file_destination_path)

        file_destination_path = self.__SHOW_DESTINATION_DIRECTORY + '/hey arnold/Season 9/hey.arnold.S09E02.SOMETHING.something-something.mp4'
        self.assertFileMoved(source_file_path_2, file_destination_path)

    def test_moving_episodes_by_name_in_directory(self):
        folder_path = self.__SOURCE_DIRECTORY + '/The.Last.Man.On.Earth.S01.Season.1.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed'
        file_handler.create_dir(folder_path)
        file_path_1 = folder_path + '/The.Last.Man.On.Earth.S01E13.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed.mkv'
        file_handler.create_file(file_path_1)

        mover.move_media_by_name(
            'The last Man On Earth',
            self.__SOURCE_DIRECTORY,
            self.__SHOW_DESTINATION_DIRECTORY,
            self.__MOVIE_DESTINATION_DIRECTORY
        )

        self.assertFileMoved(file_path_1, self.__SHOW_DESTINATION_DIRECTORY + '/The Last Man On Earth/Season 1/The.Last.Man.On.Earth.S01E13.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed.mkv')

    def test_moving_movie_by_name_in_directory(self):
        folder_path = self.__SOURCE_DIRECTORY + '/200 Cigarettes 1999.DVDRIP.Xvid.NVesub-'
        file_handler.create_dir(folder_path)
        file_path = folder_path + '/200 Cigarettes 1999.DVDRIP.Xvid.NVesub-123.mp4'
        file_handler.create_file(file_path)

        mover.move_media_by_name(
            '200 Cigarettes',
            self.__SOURCE_DIRECTORY,
            self.__SHOW_DESTINATION_DIRECTORY,
            self.__MOVIE_DESTINATION_DIRECTORY
        )

        file_destination_path = self.__MOVIE_DESTINATION_DIRECTORY + '/200 Cigarettes 1999.DVDRIP.Xvid.NVesub-123.mp4'
        self.assertFileMoved(file_path, file_destination_path)

    def test_moving_movie_in_directory(self):
        folder_path = self.__SOURCE_DIRECTORY + '/007 Going For Old Time HD-TS x264-CPG'
        file_handler.create_dir(folder_path)
        file_path = folder_path + '/007 Going For Old Time  HD-TS x264-CPG.mp4'
        file_handler.create_file(file_path)
        mover.move_media_by_path(file_path, self.__SHOW_DESTINATION_DIRECTORY, self.__MOVIE_DESTINATION_DIRECTORY)
        file_destination_path = self.__MOVIE_DESTINATION_DIRECTORY + '/007 Going For Old Time  HD-TS x264-CPG.mp4'
        self.assertFileMoved(file_path, file_destination_path)