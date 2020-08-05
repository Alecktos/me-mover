import asyncio
import logging
import unittest

from memover import logger
from memover.arguments_parser import MeMoverArgs, Commands
from memover.watcher.async_watcher import AsyncWatcher
from tests.utils import file_mover_tester

test_file_1 = 'kolla.S04E15.asswe.xTTT-RR[abf].mkv'


class TestWatcherModifiedFile(unittest.TestCase, file_mover_tester.FileMoverTester):

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    async def make_file_bigger(self):
        # modify and create file
        self._createSourceFile(test_file_1)
        self._set_size_in_mb(test_file_1, 1)

        await asyncio.sleep(1)

        # Can't assert modified_queue because it might already have been removed from queue
        # But file should never disappear from created queue if we keep modifying it
        # self.assertTrue(self.__test_file_1_path in self.my_watcher.modified_paths)
        self.assertTrue(self.__test_file_1_path in self.my_watcher.created_paths)

        # modify file
        self._set_size_in_mb(test_file_1, 1)
        await asyncio.sleep(1)

        self.assertTrue(self.__test_file_1_path in self.my_watcher.created_paths)

        # modify file
        self._set_size_in_mb(test_file_1, 1)

        await asyncio.sleep(1)

        self.assertTrue(self.__test_file_1_path in self.my_watcher.created_paths)

        # No modification to file.
        # Sleep 2 seconds to be sure that file has been moved
        await asyncio.sleep(2)

        self.assertFalse(self.__test_file_1_path in self.my_watcher.modified_paths)
        self.assertFalse(self.__test_file_1_path in self.my_watcher.created_paths)

        self._assert_file_moved(
            self.__test_file_1_path,
            f'{self._SHOW_DESTINATION_DIRECTORY}/kolla/Season 4/{test_file_1}'
        )


    def test_moving_growing_file(self):
        logger.setup(logging.DEBUG)
        self.my_watcher = None
        self.__test_file_1_path = f'{self._SOURCE_DIRECTORY}{test_file_1}'

        args = MeMoverArgs(
            Commands.WATCH,
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY,
            log_level=logging.DEBUG,
            moves_before_quit=1
        )

        loop = asyncio.get_event_loop()

        self.my_watcher = AsyncWatcher(args)

        async def run_watcher_with_growing_file():
            await asyncio.gather(
                self.my_watcher.observe(),
                self.make_file_bigger()
            )

        asyncio.run(run_watcher_with_growing_file())
