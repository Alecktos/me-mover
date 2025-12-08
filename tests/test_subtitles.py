import unittest
from memover import file_handler, subtitles, mover
from tests.utils import file_mover_tester


class TestSubtitles(unittest.TestCase, file_mover_tester.FileMoverTester):

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    def test_renaming_subs(self):
        source_files = [
            'a_movie_with_subs/Another.Another.S02E03.bigfile.mp4',
            'a_movie_with_subs/intetest/Other.Other.Other.Other.S09E01.something.something-something[something].swe.srt',
            'a_movie_with_subs/Other.Other.Other.Other.S09E01.something.something-something[something].smi',
            'a_movie_with_subs/[ www.flobbing.com ] - /Other.Other.Other.Other.S09E01.something.something-something[something].ssa',
            'a_movie_with_subs/[ www.flobbing.com ] - Longer.S01E02.HaHV.Maam-A/Information Downloaded From www.akkero.com.ass',
            'a_movie_with_subs/a/b/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig/Stuff from www.Lobertar.com.vtt',
            'a_movie_with_subs/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig/Stuff from www.Lobertar.com.txt',
            'a_movie_with_subs/intetest/Other.Other.Other.Other.S09E01.something.something-something[something].eng.srt'
        ]

        subtitles_file = [
            'a_movie_with_subs/Another.Another.S02E03.bigfile.en3.smi',
            'a_movie_with_subs/Another.Another.S02E03.bigfile.en.ass',
            'a_movie_with_subs/Another.Another.S02E03.bigfile.en5.vtt',
            'a_movie_with_subs/Another.Another.S02E03.bigfile.en4.ssa',
            'a_movie_with_subs/Another.Another.S02E03.bigfile.en2.srt',
            'a_movie_with_subs/Another.Another.S02E03.bigfile.sv.srt',
        ]

        # Create source files
        for source_file in source_files:
            self._createSourceFile(source_file)

        # make the first file the biggest
        self._set_size_in_mb(source_files[0], 60)

        subtitles.rename_and_move(self._SOURCE_DIRECTORY)

        for path in subtitles_file:
            self.assertTrue(file_handler.file_exist(self._SOURCE_DIRECTORY + path))

        #  assert that none sub files have not changed
        self.assertTrue(file_handler.file_exist(self._SOURCE_DIRECTORY + source_files[0]))

        self.assertFalse(
            file_handler.directory_exist(file_handler.get_parent(self._SOURCE_DIRECTORY + source_files[1]))
        )

        self.assertFalse(
            file_handler.file_exist(self._SOURCE_DIRECTORY + source_files[2])
        )

        self.assertFalse(
            file_handler.directory_exist(file_handler.get_parent(self._SOURCE_DIRECTORY + source_files[3]))
        )

        self.assertFalse(
            file_handler.file_exist(file_handler.get_parent(self._SOURCE_DIRECTORY + source_files[4]))
        )

        self.assertFalse(
            file_handler.directory_exist('testing/1')
        )

        self.assertTrue(file_handler.file_exist(self._SOURCE_DIRECTORY + source_files[6]))

    def test_moving_movie_with_sub_dir(self):
        class Destinations:

            def __init__(self, source, destination=None):
                self.source = source
                self.destination = destination if destination is not None else self.source

        movie_path = 'Castles.at.Sky.ghj'

        paths = [
            Destinations(movie_path + '/Castles.at.Sky.ghj.mp4'),
            Destinations(movie_path + '/Castles.at.Sky.ghj.nfo'),
            Destinations(movie_path + '/subs/English.srt', movie_path + '/Castles.at.Sky.ghj.en.srt'),
            Destinations(movie_path + '/subs/Spanish.srt', movie_path + '/Castles.at.Sky.ghj.es.srt'),
            Destinations(movie_path + '/subs/Portuguese.srt', movie_path + '/Castles.at.Sky.ghj.pt.srt'),
            Destinations(movie_path + '/subs/Swedish.srt', movie_path + '/Castles.at.Sky.ghj.sv.srt'),
            Destinations(movie_path + '/subs/Norwegian.srt', movie_path + '/Castles.at.Sky.ghj.no.srt'),
            Destinations(movie_path + '/subs/Danish.srt', movie_path + '/Castles.at.Sky.ghj.da.srt'),
            Destinations(movie_path + '/subs/Finnish.srt', movie_path + '/Castles.at.Sky.ghj.fi.srt'),
            Destinations(movie_path + '/subs/Indonesian.srt', movie_path + '/Castles.at.Sky.ghj.id.srt'),
            Destinations(movie_path + '/subs/Spanish.srt', movie_path + '/Castles.at.Sky.ghj.id.srt'),
            Destinations(movie_path + '/something_else.paa')
        ]

        for path in paths:
            self._createSourceFile(path.source)

        self._set_size_in_mb(paths[0].source, 60)

        mover.move_media_by_path(
            self._SOURCE_DIRECTORY + movie_path,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        for path in paths:
            self._assert_file_moved(path.source, self._MOVIE_DESTINATION_DIRECTORY + path.destination)
