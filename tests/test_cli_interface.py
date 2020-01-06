
# Maybe just let all the other tests
import subprocess
import unittest
import sys

from memover import argument_parser_2
from tests.utils import file_mover_tester


class TestSubtitles(unittest.TestCase, file_mover_tester.FileMoverTester):

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    def test_by_path(self):
        args = 'by-path testar testar2 testar3'

        p = subprocess.Popen(f'{sys.executable} test_cli_interface.py {args}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()
        result = output[0]
        print(result)
        self.assertEqual(b'type: by-path, source: testar, show_destination: testar2, movie_destination: testar3, quit None\n', result)


if __name__ == '__main__':
    current_args = argument_parser_2.get_current_args()
    print(current_args)