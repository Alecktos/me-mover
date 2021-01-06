import unittest

from memover.arguments_parser import MeMoverArgs, Commands
from memover.watcher.path_queue import PathQueue


class TestMoverShows(unittest.TestCase):

    __SOURCE = 'inbox'

    def setUp(self):
        self.__args = MeMoverArgs(Commands.WATCH, self.__SOURCE, 'show-destination', 'movie-destinatino')
        self.__path_queue = PathQueue(self.__args)

    def test_append_dir(self):
        path = f'before-source/{self.__SOURCE}/after-source'
        self.__path_queue.append(path)
        stripped_path = f'{self.__SOURCE}/after-source'
        self.assertEqual(self.__path_queue, [stripped_path])
        self.__path_queue.append(f'{path}/test-file.mkv')
        self.assertEqual(self.__path_queue, [stripped_path])

    def test_append_file(self):
        path = f'before-source/{self.__args.source}/test.mkv'
        self.__path_queue.append(path)
        self.assertEqual([f'{self.__args.source}/test.mkv'], self.__path_queue)

    def test_in_queue_dir(self):
        path = f'before-source/{self.__SOURCE}/after-source'
        self.__path_queue.append(path)
        self.assertTrue(self.__path_queue.in_queue(path))

        # Should only look at root dir, adding not appended file in same dir
        self.assertTrue(self.__path_queue.in_queue(f'{path}/test-file.mkv'))

    def test_in_queue_file(self):
        path = f'before-source/{self.__args.source}/test.mkv'
        self.__path_queue.append(path)
        self.assertTrue(self.__path_queue.in_queue(f'{self.__SOURCE}/test.mkv'))
