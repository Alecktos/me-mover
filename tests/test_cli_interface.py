import os
import subprocess
import sys
import unittest

from tests.utils import file_mover_tester


class TestCliInterface(unittest.TestCase, file_mover_tester.FileMoverTester):

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    def test_watch(self):
        args = 'watch test-source-watch test-show-destination-path test-movie-destination'
        result = execute(args)
        self.assertEqual(b'type: Commands.WATCH, source: test-source-watch, show_destination: test-show-destination-path, movie_destination: test-movie-destination, moves_before_quit: None, media_name: None\n', result)

    def test_watch_quit_after_moves(self):
        args = 'watch test-source-watch test-show-destination-path test-movie-destination --moves 4'
        result = execute(args)
        self.assertEqual(b'type: Commands.WATCH, source: test-source-watch, show_destination: test-show-destination-path, movie_destination: test-movie-destination, moves_before_quit: 4, media_name: None\n', result)

    def test_by_name(self):
        args = 'by-name "The name of my show " test-source-dir test-show-destination test-movie-destination'
        result = execute(args)
        self.assertEqual(b'type: Commands.BY_NAME, source: test-source-dir, show_destination: test-show-destination, movie_destination: test-movie-destination, moves_before_quit: None, media_name: The name of my show \n', result)

    def test_by_path(self):
        args = 'by-path test-source-path test-show-destination test-movie-destination'
        result = execute(args)
        self.assertEqual(b'type: Commands.BY_PATH, source: test-source-path, show_destination: test-show-destination, movie_destination: test-movie-destination, moves_before_quit: None, media_name: None\n', result)


def execute(args):
    p = subprocess.Popen(f'{sys.executable} {os.path.dirname(os.path.realpath(__file__))}/../memover/arguments_parser.py {args}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()
    result = output[0]
    print(result)
    return result
