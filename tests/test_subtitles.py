import unittest
from memover import file_handler, subtitles
from tests.utils import file_mover_tester


class MediaFileExtractorTest(unittest.TestCase, file_mover_tester.FileMoverTester):

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    def test_renaming_subs(self):
        source_files = [
            'a_movie_with_subs/test/Another.Another.S02E03.bigfile.mp4',
            'a_movie_with_subs/intetest/Other.Other.Other.Other.S09E01.something.something-something[something].swe.srt',
            'a_movie_with_subs/Other.Other.Other.Other.S09E01.something.something-something[something].smi',
            'a_movie_with_subs/[ www.flobbing.com ] - /Other.Other.Other.Other.S09E01.something.something-something[something].ssa',
            'a_movie_with_subs/[ www.flobbing.com ] - Longer.S01E02.HaHV.Maam-A/Information Downloaded From www.akkero.com.ass',
            'a_movie_with_subs/a/b/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig/Stuff from www.Lobertar.com.vtt',
            'a_movie_with_subs/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig/Stuff from www.Lobertar.com.txt',
            'a_movie_with_subs/intetest/Other.Other.Other.Other.S09E01.something.something-something[something].eng.srt'
        ]

        subtitles_file = [
            'a_movie_with_subs/test/Another.Another.S02E03.bigfile.en.smi',
            'a_movie_with_subs/test/Another.Another.S02E03.bigfile.en2.ssa',
            'a_movie_with_subs/test/Another.Another.S02E03.bigfile.en3.ass',
            'a_movie_with_subs/test/Another.Another.S02E03.bigfile.en4.vtt',
            'a_movie_with_subs/test/Another.Another.S02E03.bigfile.en5.srt',
            'a_movie_with_subs/test/Another.Another.S02E03.bigfile.en6.srt',
        ]

        for source_file in source_files:
            self._createSourceFile(source_file)

        # make the first file the biggest
        with open(self._SOURCE_DIRECTORY + source_files[0], 'wb') as bigfile:
            bigfile.seek(1048575)
            bigfile.write('0')

        subtitles.rename_and_move(self._SOURCE_DIRECTORY)

        for path in subtitles_file:
            self.assertTrue(file_handler.check_file_existance(self._SOURCE_DIRECTORY + path))

        #  assert that none sub files have not changed
        self.assertTrue(file_handler.check_file_existance(self._SOURCE_DIRECTORY + source_files[0]))

        self.assertFalse(
            file_handler.check_directory_existance(file_handler.get_parent(self._SOURCE_DIRECTORY + source_files[1]))
        )

        self.assertFalse(
            file_handler.check_file_existance(self._SOURCE_DIRECTORY + source_files[2])
        )

        self.assertFalse(
            file_handler.check_directory_existance(file_handler.get_parent(self._SOURCE_DIRECTORY + source_files[3]))
        )

        self.assertFalse(
            file_handler.check_file_existance(file_handler.get_parent(self._SOURCE_DIRECTORY + source_files[4]))
        )

        self.assertFalse(
            file_handler.check_directory_existance('testing/1')
        )

        self.assertTrue(file_handler.check_file_existance(self._SOURCE_DIRECTORY + source_files[6]))
