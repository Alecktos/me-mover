import unittest

from memover import file_handler, mover
from tests.utils import file_mover_tester


class TestMoverShows(unittest.TestCase, file_mover_tester.FileMoverTester):

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

    def test_move_shows_into_existing_season_directory(self):
        file_handler.create_dir(self._SHOW_DESTINATION_DIRECTORY + '/Kontroll US/Season 7/')
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

        file_destination_path = self._SHOW_DESTINATION_DIRECTORY + '/Kontroll US/Season 7/' + tv_show_file_name
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

        self.__create_move_and_validate_season1_episodes(episodes, show_name)

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

        self.__create_move_and_validate_season1_episodes(episodes, show_name)

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

        self.__create_move_and_validate_season1_episodes(episodes, show_name)

    def test_moving_one_season_different_episodes_naming_schemes_1(self):
        show_name = 'First Test [ONE_SEASON_DIFFERENT_NAMING_SCHEMES]/'

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

        self.__create_move_and_validate_season1_episodes(episodes, show_name)

    def test_moving_one_season_different_episodes_naming_schemes_2(self):

        show_name = 'Second Test [ONE_SEASON_DIFFERENT_NAMING_SCHEMES]/'

        episodes = (
            '[ATBC] Jkl Jkl Jkl Jkl Has - 01[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 02[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 03[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 04[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 05[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 06[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 07v2[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 08[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 09[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 10v2[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 11v2[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 12[1233].mkv',
            '[ATBC] Jkl Jkl Jkl Jkl Has - 13[1233].mkv'
        )

        self.__create_move_and_validate_season1_episodes(episodes, show_name)

    def test_moving_one_season_different_episodes_naming_schemes_3(self):

        show_name = 'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES/'

        episodes = (
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 01 (1920x1080 HEVC2 EAC3).mks',
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 01 (1920x1080 HEVC2 EAC3).mkv',
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 02 (1920x1080 HEVC2 EAC3).mks',
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 02 (1920x1080 HEVC2 EAC3).mkv',
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 03 (1920x1080 HEVC2 EAC3).mks',
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 03 (1920x1080 HEVC2 EAC3).mkv',
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 04 (1920x1080 HEVC2 EAC3).mks',
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 04 (1920x1080 HEVC2 EAC3).mkv',
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 05 (1920x1080 HEVC2 EAC3).mks',
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 05 (1920x1080 HEVC2 EAC3).mkv',
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 06 (1920x1080 HEVC2 EAC3).mks',
            'Third Test ONE_SEASON_DIFFERENT_NAMING_SCHEMES - 06 (1920x1080 HEVC2 EAC3).mkv'
        )

        self.__create_move_and_validate_season1_episodes(episodes, show_name)

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

        self.__create_move_and_validate_season1_episodes(episodes, show_name)

    def test_moving_episode_short(self):
        show_name = "Storage Found (1080p A789 10bit dksala)/"

        meta_root_files = (
            'fjdksl a-Alkh AJKL Alkerra JKl Alle akl dajs.website'
            'Ander kl Oker.txt',
            'Jk jk hjkl AHV (jkl Ahtt).txt',
        )

        for file in meta_root_files:
            self._createSourceFile(show_name + file)

        episodes = (
            'Storage Found E02 Ahe jdksle osaf fjdskljkl (1080p A789 10bit dksala).mkv',
            'Storage Found E06 Ass Frdsaosdsaty (1080p A789 10bit dksala).mkv',
            'Storage Found E04 Codsambat Jdasacak (1080p A789 10bit dksala).mkv',
            'Storage Found E07 Bodsambda idsan thdsae Gadasrdsadddden (1080p A789 10bit dksala).mkv',
            'Storage Found E01 Gdsadsae dame (1080p A789 10bit dksala).mkv',
            'Storage Found E05 A dsasaaaa Cat (1080p A789 10bit dksala).mkv',
            'Storage Found E03 Sounding (1080p A789 10bit dksala).mkv'
        )
        self.__create_move_and_validate_season1_episodes(episodes, show_name)

        for file in meta_root_files:
            self._assert_file_moved(show_name + file, self._SHOW_DESTINATION_DIRECTORY + show_name + file)

    def test_same_show_name_on_each_file(self):
        show_source_dir = 'kung fo season 1 (1080p bd 123)/'
        destination_show_path = self._SHOW_DESTINATION_DIRECTORY + '/Kung Fo/Season 1/'

        file_name_1 = 'Kung fo S01E01 Completely Strange (1080p) (C).mkv'
        file_name_2 = '(C) for Audio Commentary.txt'
        file_name_3 = 'Kung fo S01E02 Somewhat Stranger (1080p) (C).mkv'

        file_handler.create_dir(destination_show_path)

        self._createSourceFile(show_source_dir + file_name_1)
        self._createSourceFile(show_source_dir + file_name_2)
        self._createSourceFile(show_source_dir + file_name_3)

        mover.move_media_by_path(
            self._SOURCE_DIRECTORY + show_source_dir,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        self._assert_file_moved(show_source_dir + file_name_1, destination_show_path + file_name_1)
        self._assert_file_moved(show_source_dir + file_name_2, self._SHOW_DESTINATION_DIRECTORY + '/Kung Fo/' + file_name_2)
        self._assert_file_moved(show_source_dir + file_name_3, destination_show_path + file_name_3)

    def test_screens_images_moved_correctly(self):
        show_name = 'what happens in the sun/'
        show_source_dir = '/What Happens in the Sun S01E01 1080p WEB H264'
        source_show_dir = self._SOURCE_DIRECTORY + show_source_dir

        file_handler.create_dir(source_show_dir)
        episode = '/what.happens.in.the.sun.s01e01.1080p.web.h264.mkv'
        file_handler.create_file(source_show_dir + episode)

        screen_dir = '/Screens'
        file_handler.create_dir(source_show_dir + screen_dir)
        screen_file = '/screen0001.jpg'
        file_handler.create_file(source_show_dir + screen_dir + screen_file)

        mover.move_media_by_path(
            source_show_dir,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        self._assert_file_moved(source_show_dir + screen_dir + screen_file, self._SHOW_DESTINATION_DIRECTORY + show_name + screen_file)

        self.__validate_episodes_season_1([episode], show_name)

    def test_multiple_matches(self):
        file_handler.create_dir(f'{self._SHOW_DESTINATION_DIRECTORY}mr test')
        file_handler.create_dir(f'{self._SHOW_DESTINATION_DIRECTORY}Test Test and Test')

        episode_name = 'Mr.Test.S07E01.REPACK.a111-AAA[a]'
        file_handler.create_dir(f'{self._SOURCE_DIRECTORY}{episode_name}')
        file_path = f'{self._SOURCE_DIRECTORY}{episode_name}/{episode_name}.mp4'
        file_handler.create_file(file_path)

        mover.move_media_by_path(
            self._SOURCE_DIRECTORY + episode_name,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        self._assert_file_moved(
            file_path,
            f'{self._SHOW_DESTINATION_DIRECTORY}mr test/Season 7/{episode_name}.mp4'
        )

    def test_title_in_file_name(self):
        show_name = 'Mr Wayne A Ale & Faber in The Cure/'

        episodes = [
            'Title 01 - Some title 1.mp4',
            'Title 02 - Some title 2.mp4',
            'Title 03 - Some title 3.mp4',
            'Title 04 - Some title 4.mp4',
            'Title 05 - Some title 5.mp4',
            'Title 06 - Some title 6.mp4'
        ]

        self.__create_move_and_validate_season1_episodes(episodes, show_name)

    def __create_move_and_validate_season1_episodes(self, episodes, show_name):
        for episode in episodes:
            file_path = show_name + episode
            self._createSourceFile(file_path)
            self._set_size_in_mb(file_path, 50)

        mover.move_media_by_path(
            self._SOURCE_DIRECTORY + show_name,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )
        self.__validate_episodes_season_1(episodes, show_name)

    def __validate_episodes_season_1(self, episodes, show_name):
        for episode in episodes:
            self._assert_file_moved(show_name + episode, self._SHOW_DESTINATION_DIRECTORY + show_name + 'Season 1/' + episode)
