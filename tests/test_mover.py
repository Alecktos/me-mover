import unittest
from tests.utils import file_mover_tester
from memover import file_handler, mover


class MoverTest(unittest.TestCase, file_mover_tester.FileMoverTester):

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    def test_move_show_by_name(self):
        tv_show_file_name = 'All.the.Things.Fire.S02E10.720p.SOMETHING.something-SOMETHING.mkv'
        file_handler.create_file(self._SOURCE_DIRECTORY + tv_show_file_name)

        mover.move_media_by_name(
            'all the things fire',
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        destination_path = self._SHOW_DESTINATION_DIRECTORY + '/All the Things Fire/Season 2/' + tv_show_file_name
        file_is_in_new_path = file_handler.file_exist(destination_path)
        self.assertTrue(file_is_in_new_path)

        source_path = self._SOURCE_DIRECTORY + '/' + tv_show_file_name
        file_is_in_old_path = file_handler.file_exist(source_path)
        self.assertFalse(file_is_in_old_path)

    def test_move_show_by_file_path(self):
        tv_show_file_name = 'Man.In.The.on.Folder.S02E03.Dead.AAA.Walking.Wrong-DL.x123.BBA.mp4'
        file_handler.create_file(self._SOURCE_DIRECTORY + '/' + tv_show_file_name)

        source_file_path = self._SOURCE_DIRECTORY + '/' + tv_show_file_name
        mover.move_media_by_path(source_file_path, self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)

        destination_path = self._SHOW_DESTINATION_DIRECTORY + '/Man In The on Folder/Season 2/' + tv_show_file_name
        self._assert_file_moved(source_file_path, destination_path)

    def test_move_movie_by_file_path(self):
        movie_file_name = 'Abcde Fgh ijk Wjere To Found In 2010 HD-AA x111-ABC.mkv'
        file_handler.create_file(self._SOURCE_DIRECTORY + '/' + movie_file_name)

        source_file_path = self._SOURCE_DIRECTORY + '/' + movie_file_name
        mover.move_media_by_path(source_file_path, self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)

        destination_path = self._MOVIE_DESTINATION_DIRECTORY + '/' + file_handler.get_last_name_from_path(movie_file_name) + '/' + movie_file_name
        self._assert_file_moved(source_file_path, destination_path)

    def test_move_shows_into_existing_season_directory(self):
        # Test with two letter word in the end of file name that should be stripped
        file_handler.create_dir(self._SHOW_DESTINATION_DIRECTORY + '/Kontroll/Season 7/')
        tv_show_file_name = 'kontroll.US.S07E02.720p.AM.SOMETING-OTHER-DEMINSION[aaa]'
        file_source_path = self._SOURCE_DIRECTORY + '/' + tv_show_file_name
        file_handler.create_file(file_source_path)

        # move by name
        mover.move_media_by_name(
            'kontroll',
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        file_destination_path = self._SHOW_DESTINATION_DIRECTORY + '/Kontroll/Season 7/' + tv_show_file_name
        self._assert_file_moved(file_source_path, file_destination_path)

        # move by file
        file_handler.delete_file(file_destination_path)
        file_handler.create_file(file_source_path)
        mover.move_media_by_path(file_source_path, self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)
        self._assert_file_moved(file_source_path, file_destination_path)

        # Test with two letter word in the middle of file name that should not be stripped when matching
        file_handler.create_dir(self._SHOW_DESTINATION_DIRECTORY + '/Cool And Welcome To Earth/Season 2/')
        tv_show_file_name = 'Cool.And.Welcome.To.Earth.S02E02.The.Boo.720p.KOL-OL.A300.MP#.mp4'
        file_source_path = self._SOURCE_DIRECTORY + '/' + tv_show_file_name
        file_handler.create_file(file_source_path)

        mover.move_media_by_name(
            'Cool And Welcome To Earth',
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        file_destination_path = self._SHOW_DESTINATION_DIRECTORY + '/Cool And Welcome To Earth/Season 2/' + tv_show_file_name
        self._assert_file_moved(file_source_path, file_destination_path)

    def test_moving_episodes_by_file_in_directory(self):
        folder_path = self._SOURCE_DIRECTORY + 'hey.arnold.season1.720p.webdl'
        file_handler.create_dir(folder_path)
        source_file_path_1 = folder_path + '/hey.arnold.S09E01.SOMETHING.something-something'
        file_handler.create_file(source_file_path_1)

        source_file_path_2 = folder_path + '/hey.arnold.S09E02.SOMETHING.something-something.mp4'
        file_handler.create_file(source_file_path_2)

        mover.move_media_by_path(folder_path, self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)

        file_destination_path = self._SHOW_DESTINATION_DIRECTORY + '/hey arnold/Season 9/hey.arnold.S09E01.SOMETHING.something-something'
        self._assert_file_moved(source_file_path_1, file_destination_path)

        file_destination_path = self._SHOW_DESTINATION_DIRECTORY + '/hey arnold/Season 9/hey.arnold.S09E02.SOMETHING.something-something.mp4'
        self._assert_file_moved(source_file_path_2, file_destination_path)

    def test_moving_episodes_by_name_in_directory(self):
        folder_path = self._SOURCE_DIRECTORY + '/Cool.And.Welcome.To.Earth.S01.Season.1.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed'
        file_handler.create_dir(folder_path)
        file_path_1 = folder_path + '/Cool.And.Welcome.To.Earth.S01E13.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed.mkv'
        file_handler.create_file(file_path_1)

        mover.move_media_by_name(
            'Cool And Welcome To Earth',
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        self._assert_file_moved(file_path_1, self._SHOW_DESTINATION_DIRECTORY + 'Cool And Welcome To Earth/Season 1/Cool.And.Welcome.To.Earth.S01E13.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed.mkv')

    def test_moving_movie_in_directory(self):
        folder_path = self._SOURCE_DIRECTORY + '007 Going For Old Time HD-TS x264-CPG'
        file_handler.create_dir(folder_path)
        file_path = folder_path + '/007 Going For Old Time  HD-TS x264-CPG.mp4'
        file_handler.create_file(file_path)
        mover.move_media_by_path(file_path, self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)
        file_destination_path = self._MOVIE_DESTINATION_DIRECTORY + '/007 Going For Old Time  HD-TS x264-CPG/007 Going For Old Time  HD-TS x264-CPG.mp4'
        self._assert_file_moved(file_path, file_destination_path)

    def test_moving_movie_with_image(self):
        folder_path = self._SOURCE_DIRECTORY + 'Konstig (2017) [1080p] [JKL.KL]'
        file_handler.create_dir(folder_path)
        source_file_path = folder_path + '/WWW.YTS.AG.jpg'
        file_handler.create_file(source_file_path)

        mover.move_media_by_path(folder_path, self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)

        file_destination_path = self._MOVIE_DESTINATION_DIRECTORY + '/Konstig (2017) [1080p] [JKL.KL]/WWW.YTS.AG.jpg'
        self._assert_file_moved(source_file_path, file_destination_path)

    def test_moving_movies_by_name(self):
        file_1_folder_path = self._SOURCE_DIRECTORY + '/201 Coolings 1999.DVDRIP.Xvid.NVesub-'
        file_handler.create_dir(file_1_folder_path)
        file_1_path = file_1_folder_path + '/201 Coolings 1999.___RIP.Xvid.NVesub-123.mp4'
        file_handler.create_file(file_1_path)

        file_2_path = self._SOURCE_DIRECTORY + '/201 Coolings 200.DADRAP.NVesub.mp4'
        file_handler.create_file(file_2_path)

        mover.move_media_by_name(
            '201 Coolings',
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        file_destination_path = self._MOVIE_DESTINATION_DIRECTORY + '/201 Coolings 1999.DVDRIP.Xvid.NVesub-/201 Coolings 1999.___RIP.Xvid.NVesub-123.mp4'
        self._assert_file_moved(file_1_folder_path, file_destination_path)

        file_destination_path = self._MOVIE_DESTINATION_DIRECTORY + '/201 Coolings 200.DADRAP.NVesub/201 Coolings 200.DADRAP.NVesub.mp4'
        self._assert_file_moved(file_2_path, file_destination_path)

    def test_moving_wrong_formatted_episode_inside_right_formated_directory(self):
        folder_path = self._SOURCE_DIRECTORY + '/My.Stuff.Us.On.S10E09.HDTV.CCCC-ARD[axel]'
        source_path = self._createSourceFile(folder_path + '/my.stuff.us.on.1009.fktv-uuu[axel].mkv')

        mover.move_media_by_path(source_path, self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)
        self._assert_file_moved(folder_path, self._SHOW_DESTINATION_DIRECTORY + '/My Stuff Us On/Season 10/my.stuff.us.on.1009.fktv-uuu[axel].mkv')

    def test_moving_episode_in_season_dir(self):
        folder_path = 'Kan Inte/Season 3/'
        file_name = 'Kan Inte S03E02 Apptest'
        source_path = self._createSourceFile(folder_path + file_name)
        mover.move_media_by_path(self._SOURCE_DIRECTORY + 'Kan Inte', self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)
        self._assert_file_moved(source_path, self._SHOW_DESTINATION_DIRECTORY + '/' + folder_path + file_name)

    def test_moving_multiple_episodes_with_subtitles_and_instruction_file(self):
        self._createSourceFile('Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV.srt')
        self._createSourceFile('Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV.mkv')
        self._set_size_in_mb('Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV.mkv', 60)

        self._createSourceFile('Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV.srt')
        self._createSourceFile('Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV.mkv')
        self._set_size_in_mb('Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV.mkv', 61)

        self._createSourceFile('Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV.srt')
        self._createSourceFile('Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV.mkv')
        self._set_size_in_mb('Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV.mkv', 62)

        self._createSourceFile('Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Instructions.txt')

        mover.move_media_by_path(self._SOURCE_DIRECTORY + 'Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p', self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)

        self._assert_file_moved(
            'Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV.srt',
            'show-destination/Kalla Rander, Valla Calla/Season 1/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV.en.srt'
        )

        self._assert_file_moved(
            'Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV.mkv',
            'show-destination/Kalla Rander, Valla Calla/Season 1/Kalla Rander, Valla Calla S01E01 (Generationen X) HDTV.mkv'
        )

        self._assert_file_moved(
            'Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV.srt',
            'show-destination/Kalla Rander, Valla Calla/Season 1/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV.en.srt'
        )

        self._assert_file_moved(
            'Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV.mkv',
            'show-destination/Kalla Rander, Valla Calla/Season 1/Kalla Rander, Valla Calla S01E02 (Generationen X) HDTV.mkv'
        )

        self._assert_file_moved(
            'Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV.srt',
            'show-destination/Kalla Rander, Valla Calla/Season 1/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV.en.srt'
        )

        self._assert_file_moved(
            'Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV.mkv',
            'show-destination/Kalla Rander, Valla Calla/Season 1/Kalla Rander, Valla Calla S01E03 (Generationen X) HDTV.mkv'
        )

        self._assert_file_moved(
            'Kalla Rander, Valla Calla S01 (Generationen X) HDTV 720p/Instructions.txt',
            'show-destination/Kalla Rander, Valla Calla/Season 1/Instructions.txt'
        )

    def test_moving_show_different_naming_scheme(self):
        episodes = (
            'Last Last - 1x01 - [123].mkv',
            'Last Last - 1x02 - [123].mkv',
            'Last Last - 1x03 - [123].mkv',
            'Last Last - 1x04 - [123].mkv',
            'Last Last - 1x05 - [123].mkv',
            'Last Last - 1x06 - [123].mkv',
            'Last Last - 1x07 - [123].mkv',
            'Last Last - 1x08 - [123].mkv',
            'Last Last - 1x09 - [123].mkv',
            'Last Last - 1x09 - [123].mkv',
            'Last Last - 1x10 - [123].mkv',
            'Last Last - 1x11 - [123].mkv',
            'Last Last - 1x12 - [123].mkv',
            'Last Last - 1x13 - [123].mkv',
            'Last Last - 1x14 - [123].mkv',
            'Last Last - 1x15 - [123].mkv',
            'Last Last - 1x16 - [123].mkv',
            'Last Last - 1x17 - [123].mkv',
            'Last Last - 1x18 - [123].mkv',
            'Last Last - 1x19 - [123].mkv',
            'Last Last - 1x20 - [123].mkv',
            'Last Last - 1x21 - [123].mkv',
            'Last Last - 1x22 - [123].mkv',
            'Last Last - 1x23 - [123].mkv',
            'Last Last - 1x24 - [123].mkv',
            'Last Last - 1x25 - [123].mkv',
            'Last Last - 1x26 - [123].mkv'
        )
        show_name = 'Last Last/'

        self.__validate_season_1_moved(episodes, show_name)

    def test_moving_one_season_only_show(self):
        episodes = (
            '[SyS] Wall Hunger 01 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 02 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 03 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 04 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 05 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 06 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 07 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 08 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 09 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 10 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 11 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 12 (AA 1920x1080 s125 FLAC) [].mkv',
            '[SyS] Wall Hunger 13 (AA 1920x1080 s125 FLAC) [].mkv'
        )

        show_name = '[SyS] Wall Hunger/'

        self.__validate_season_1_moved(episodes, show_name)

        episodes = (
            '[ABA]_and_and_axa_-_01_-_Ijfdsklalllk_[720p]_[ghjk].mkv',
            '[ABA]_and_and_axa_-_02_-_Ijfdsklalllk_[720p]_[ghjk].mkv',
            '[ABA]_and_and_axa_-_03_-_Ijfdsklalllk_[720p]_[ghjk].mkv',
            '[ABA]_and_and_axa_-_04_-_Ijfdsklalllk_[720p]_[ghjk].mkv',
            '[ABA]_and_and_axa_-_05_-_IjfdsklalllkGirlfriend_[720p]_[ghjk].mkv',
            '[ABA]_and_and_axa_-_06_-_Ijfdsklalllk_[720p]_[ghjk].mkv',
            '[ABA]_and_and_axa_-_07_-_Ijfdsklalllk_[720p]_[ghjk].mkv',
            '[ABA]_and_and_axa_-_08_-_Ijfdsklalllk_[720p]_[ghjk].mkv',
            '[ABA]_and_and_axa_-_09_-_Ijfdsklalllk_[720p]_[ghjk].mkv',
            '[ABA]_and_and_axa_-_10_-_The_Shosasa_[720p]_[ghjk].mkv',
            '[ABA]_and_and_axa_-_11_-_The_Ad_Battle_Contin_[720p]_[ghjk].mkv',
            '[ABA]_and_and_axa_-_12_-_Ijfdsklalllk_[720p]_[ghjk].mkv'
        )

        show_name = '[ABA]_and_and_axa_-/'  # for now show name will be stripped just before episode

        self.__validate_season_1_moved(episodes, show_name)

    def test_moving_one_season_different_naming_schemes(self):
        show_name = 'Kande inte [Flera-Audio]/'

        episodes = (
            '01 - djksalo-jjjSub].mkv',
            '02 - djksalo-jjjulti-Sub].mkv',
            '03 - djksalo-jjjSub].mkv',
            '04 - djksalo-jjjSub].mkv',
            '05 - djksalo-jjjub].mkv',
            '06 - djksalo-jjjulti-Sub].mkv',
            '07 - djksalo-jjj[Multi-Sub].mkv',
            '08 - djksalo-jjjulti-Sub].mkv',
            '09 - djksalo-jjjudio][Multi-Sub].mkv',
            '10 - djksalo-jjj.mkv'
        )

        self.__validate_season_1_moved(episodes, show_name)

    def test_moving_with_only_season(self):
        episode = 'Lisa.Mirrander.S02.Special.Rocked.Summer.1080p.WEB-Org.AA02.1.LKIO.mkv'
        self._createSourceFile(episode)
        mover.move_media_by_path(self._SOURCE_DIRECTORY + episode, self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)
        self._assert_file_moved(episode, self._SHOW_DESTINATION_DIRECTORY + 'Lisa Mirrander/Season 2/' + episode)

    def test_moving_with_episode_in_file_name(self):
        show_name = 'Al Ber II aew Color/'

        episodes = (
            'Episode 01 - fhdsjk.avi',
            'Episode 02 - The Ale djs.avi',
            'Episode 03 - Alw at as.avi',
            'Episode 04 - hdsk fjdsl dss.avi',
            'Episode 05 - Areda Aa Kanske.avi',
            'Episode 06 - The Felaktig ocd Nord More.avi',
            'Episode 07 - Stong the Ring.avi'
        )

        self.__validate_season_1_moved(episodes, show_name)

    def __validate_season_1_moved(self, episodes, show_name):

        for episode in episodes:
            file_path = show_name + episode
            self._createSourceFile(file_path)
            self._set_size_in_mb(file_path, 50)

        mover.move_media_by_path(
            self._SOURCE_DIRECTORY + show_name,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        for episode in episodes:
            self._assert_file_moved(show_name + episode, self._SHOW_DESTINATION_DIRECTORY + show_name + 'Season 1/' + episode)
