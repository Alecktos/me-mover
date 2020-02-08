import asyncio
import unittest

from memover.arguments_parser import MeMoverArgs, Commands
from memover.watcher.async_watcher import AsyncWatcher
from tests.utils import file_mover_tester

auto_turn_off = 4  # in seconds
test_file_1 = 'kolla.S04E15.asswe.xTTT-RR[abf].mkv'
test_file_2 = 'kolla.S05E16.asswe.xTTT-RR[abf].mkv'


class TestWatcherModifiedFile(unittest.TestCase, file_mover_tester.FileMoverTester):

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    async def make_file_bigger(self):
        await asyncio.sleep(1)

        self._createSourceFile(test_file_1)
        self._set_size_in_mb(test_file_1, 2)

        await asyncio.sleep(1)

        self.assertTrue(self.__test_file_1_path in self.my_watcher.modified_paths)
        self.assertTrue(self.__test_file_1_path in self.my_watcher.created_paths)

        await asyncio.sleep(1)

        self._set_size_in_mb(test_file_1, 2)

        await asyncio.sleep(1)

        self._set_size_in_mb(test_file_1, 2)

        await asyncio.sleep(1)

        self.assertFalse(self.__test_file_1_path in self.my_watcher.modified_paths)
        self.assertFalse(self.__test_file_1_path in self.my_watcher.created_paths)

    def test_moving_growing_file(self):
        self.my_watcher = None
        self.__test_file_1_path = f'{self._SOURCE_DIRECTORY}{test_file_1}'

        args = MeMoverArgs(
            Commands.WATCH,
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY,
            auto_turn_off
        )

        loop = asyncio.get_event_loop()

        self.my_watcher = AsyncWatcher(args)

        all_groups = asyncio.gather(
            self.make_file_bigger(),
            self.my_watcher.observe(),
            self.my_watcher.move_created_files()
        )

        results = loop.run_until_complete(all_groups)
        loop.close()  # It's possible that'm using thwe old asyncio API here.
