import unittest
from memover import file_handler, subtitles


class MediaFileExtractorTest(unittest.TestCase):

    __SOURCE_FILES = [
        'testing/test/Another.Another.S02E03.bigfile.mp4',
        'testing/intetest/Other.Other.Other.Other.S09E01.something.something-something[something].swe.srt',
        'testing/Other.Other.Other.Other.S09E01.something.something-something[something].smi',
        'testing/[ www.flobbing.com ] - /Other.Other.Other.Other.S09E01.something.something-something[something].ssa',
        'testing/[ www.flobbing.com ] - Longer.S01E02.HaHV.Maam-A/Information Downloaded From www.akkero.com.ass',
        'testing/a/b/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig/Stuff from www.Lobertar.com.vtt',
        'testing/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig/Stuff from www.Lobertar.com.txt',
        'testing/intetest/Other.Other.Other.Other.S09E01.something.something-something[something].eng.srt'
    ]

    __SUBTITLES_FILES = [
        'testing/test/Another.Another.S02E03.bigfile.en.smi',
        'testing/test/Another.Another.S02E03.bigfile.en2.ssa',
        'testing/test/Another.Another.S02E03.bigfile.en3.ass',
        'testing/test/Another.Another.S02E03.bigfile.en4.vtt',
        'testing/test/Another.Another.S02E03.bigfile.en5.srt',
        'testing/test/Another.Another.S02E03.bigfile.en6.srt',
    ]

    def tearDown(self):
        file_handler.delete_directory('testing')

    def test_renaming_subs(self):
        file_handler.create_dir('testing/test')
        file_handler.create_dir('testing/intetest')
        file_handler.create_dir('testing/[ www.flobbing.com ] - ')
        file_handler.create_dir('testing/[ www.flobbing.com ] - Longer.S01E02.HaHV.Maam-A')
        file_handler.create_dir('testing/a/b/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig')
        file_handler.create_dir('testing/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig')
        for path in self.__SOURCE_FILES:
            file_handler.create_file(path)

        # make the first file the biggest
        with open(self.__SOURCE_FILES[0], 'wb') as bigfile:
            bigfile.seek(1048575)
            bigfile.write('0')

        subtitles.rename_and_move('testing')

        for path in self.__SUBTITLES_FILES:
            self.assertTrue(file_handler.check_file_existance(path))

        #  assert that none sub files have not changed
        self.assertTrue(file_handler.check_file_existance(self.__SOURCE_FILES[0]))

        self.assertFalse(
            file_handler.check_directory_existance(file_handler.get_parent(self.__SOURCE_FILES[1]))
        )

        self.assertFalse(
            file_handler.check_file_existance(self.__SOURCE_FILES[2])
        )

        self.assertFalse(
            file_handler.check_directory_existance(file_handler.get_parent(self.__SOURCE_FILES[3]))
        )

        self.assertFalse(
            file_handler.check_file_existance(file_handler.get_parent(self.__SOURCE_FILES[4]))
        )

        self.assertFalse(
            file_handler.check_directory_existance('testing/1')
        )

        self.assertTrue(file_handler.check_file_existance(self.__SOURCE_FILES[6]))
