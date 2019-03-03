import unittest
from memover import file_handler
from tests.utils import file_mover_tester


class TestFileHandler(unittest.TestCase, file_mover_tester.FileMoverTester):

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    def test_get_path_without_extension(self):
        path = 'ColdCraft (2016) FinSub CDROMRip x264 KORIG'
        result = file_handler.get_path_without_extension(path)
        self.assertEqual(path, result)

    def test_get_biggest_file(self):
        file_path = self._createSourceFile('a/b/c/d/e/f/g.aa')
        directory_path = file_handler.get_parent(file_path)
        biggest_files = list(file_handler.get_biggest_files(directory_path, self._SOURCE_DIRECTORY))
        self.assertEqual(1, len(biggest_files))
        self.assertEqual(file_path, biggest_files[0].path)
