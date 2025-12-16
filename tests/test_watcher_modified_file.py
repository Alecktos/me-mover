import asyncio
import logging
import unittest

from memover import logger
from memover.arguments_parser import MeMoverArgs, Commands
from memover.watcher.async_watcher import AsyncWatcher
from tests.utils import file_mover_tester


class TestWatcherModifiedFile(unittest.TestCase, file_mover_tester.FileMoverTester):

    @property
    def test_file_1(self):
        return 'kolla.S04E15.asswe.xTTT-RR[abf].mkv'

    @property
    def test_file_1_path(self):
        return f'{self._SOURCE_DIRECTORY}{self.test_file_1}'

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    async def make_file_bigger(self):
        # modify and create file
        self._createSourceFile(self.test_file_1)
        self._set_size_in_mb(self.test_file_1, 1)

        await asyncio.sleep(AsyncWatcher.SLEEP_SECONDS)

        self.assertEqual(self.my_watcher.created_paths, [self.test_file_1_path])

        # modify file
        self._set_size_in_mb(self.test_file_1, 1)
        await asyncio.sleep(AsyncWatcher.SLEEP_SECONDS)

        self.assertEqual(self.my_watcher.created_paths, [self.test_file_1_path])

        # modify file
        self._set_size_in_mb(self.test_file_1, 1)

        await asyncio.sleep(AsyncWatcher.SLEEP_SECONDS + 1)

        self.assertEqual(self.my_watcher.created_paths, [self.test_file_1_path])

        # No modification to file.
        # Sleep longer to be sure that file has been moved
        await asyncio.sleep(AsyncWatcher.SLEEP_SECONDS + 1)

        self.assertEqual(self.my_watcher.created_paths, [])

        self._assert_file_moved(
            self.test_file_1,
            f'{self._SHOW_DESTINATION_DIRECTORY}/kolla/Season 4/{self.test_file_1}'
        )

    def test_moving_growing_file(self):
        logger.setup(logging.DEBUG)
        self.my_watcher = None

        args = MeMoverArgs(
            Commands.WATCH,
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY,
            log_level=logging.DEBUG,
            moves_before_quit=1
        )

        self.my_watcher = AsyncWatcher(args, stable_seconds=0)

        async def run_watcher_with_growing_file():
            await asyncio.gather(
                self.my_watcher.observe(),
                self.make_file_bigger()
            )

        asyncio.run(run_watcher_with_growing_file())
