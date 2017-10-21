import unittest
from memover import file_handler, subtitles_renamer


class MediaFileExtractorTest(unittest.TestCase):

    __SOURCE_FILES = [
        'testar/test/Another.Another.S02E03.bigfile.mp4',
        'testar/intetest/Other.Other.Other.Other.S09E01.something.something-something[something].srt',
        'testar/Other.Other.Other.Other.S09E01.something.something-something[something].smi',
        'testar/[ www.flobbing.com ] - /Other.Other.Other.Other.S09E01.something.something-something[something].ssa',
        'testar/[ www.flobbing.com ] - Longer.S01E02.HaHV.Maam-A/Information Downloaded From www.akkero.com.ass',
        'testar/a/b/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig/Stuff from www.Lobertar.com.vtt'
        'testar/www.Lobertar.com - Long.S01E02.720p.KOOK.asdf-Risig/Stuff from www.Lobertar.com.txt'
    ]

    __SUBTITLES_FILES = [
        'testar/Another.Another.S02E03.bigfile.srt',
        'testar/Another.Another.S02E03.bigfile.smi',
        'testar/Another.Another.S02E03.bigfile.ssa',
        'testar/Another.Another.S02E03.bigfile.ass',
        'testar/Another.Another.S02E03.bigfile.vtt'
    ]

    def test_renaming_subs(self):
        for path in self.__SOURCE_FILES:
            file_handler.create_file(path)

        # make the first file the biggest
        with open(self.__SOURCE_FILES[0], 'wb') as bigfile:
            bigfile.seek(1048575)
            bigfile.write('0')

        subtitles_renamer.rename('testar/')

        for path in self.__SOURCE_FILES:
            self.assertTrue(file_handler.check_file_existance(path))

        #  assert that none sub files have not changed
        self.assertTrue(file_handler.check_file_existance(self.__SOURCE_FILES[0]))
        self.assertTrue(file_handler.check_file_existance(self.__SOURCE_FILES[6]))
