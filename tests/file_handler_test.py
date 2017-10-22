import unittest
from memover import file_handler


class MediaFileExtractorTest(unittest.TestCase):

    def test_get_path_without_extension(self):
        path = 'ColdCraft (2016) FinSub CDROMRip x264 KORIG'
        result = file_handler.get_path_without_extension(path)
        self.assertEqual(path, result)
