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
        self.__path_queue.append(path, 1000.0)
        stripped_path = f'{self.__SOURCE}/after-source'
        self.assertEqual(self.__path_queue, [stripped_path])
        self.__path_queue.append(f'{path}/test-file.mkv', 1000.0)
        self.assertEqual(self.__path_queue, [stripped_path])

    def test_append_file(self):
        path = f'before-source/{self.__args.source}/test.mkv'
        self.__path_queue.append(path, 1000.0)
        self.assertEqual([f'{self.__args.source}/test.mkv'], self.__path_queue)

    def test_in_queue_dir(self):
        path = f'before-source/{self.__SOURCE}/after-source'
        self.__path_queue.append(path, 1000.0)
        self.assertTrue(self.__path_queue.in_queue(path))

        # Should only look at root dir, adding not appended file in same dir
        self.assertTrue(self.__path_queue.in_queue(f'{path}/test-file.mkv'))

    def test_in_queue_file(self):
        path = f'before-source/{self.__args.source}/test.mkv'
        self.__path_queue.append(path, 1000.0)
        self.assertTrue(self.__path_queue.in_queue(f'{self.__SOURCE}/test.mkv'))

    def test_get_timestamp(self):
        path = f'before-source/{self.__SOURCE}/media-file-path'
        self.__path_queue.append(path, 1000.0)
        self.assertEqual(1000.0, self.__path_queue.get_last_modified(path))

    def test_get_timestamp_not_found(self):
        path = f'before-source/{self.__SOURCE}/media-file-path'
        self.assertIsNone(self.__path_queue.get_last_modified(path))

    def test_update_last_modified(self):
        path = f'before-source/{self.__SOURCE}/media-file-path'
        self.__path_queue.append(path, 1000.0)
        self.__path_queue.update_last_modified(path, 2000.0)
        self.assertEqual(2000.0, self.__path_queue.get_last_modified(path))

    def test_time_since_last_modify(self):
        path = f'before-source/{self.__SOURCE}/media-file-path'
        self.__path_queue.append(path, 1000.0)
        self.assertEqual(500.0, self.__path_queue.time_since_last_modified(path, 1500.0))

    def test_time_since_last_modify_not_found(self):
        path = f'before-source/{self.__SOURCE}/media-file-path'
        self.assertIsNone(self.__path_queue.time_since_last_modified(path, 1500.0))
