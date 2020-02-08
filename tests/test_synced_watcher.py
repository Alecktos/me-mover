import unittest

from memover.arguments_parser import MeMoverArgs, Commands
from memover.watcher.async_watcher import SyncedWatcher
from tests.utils import file_mover_tester


class TestSyncedWatcher(unittest.TestCase, file_mover_tester.FileMoverTester):

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    def test_only_root_added_queues(self):
        episode_name = 'kolla.S04E15.asswe.xTTT-RR[abf]'

        args = MeMoverArgs(
            Commands.WATCH,
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        synced_watcher = SyncedWatcher(args)

        # Create dir
        dir_1 = self._create_source_dir(episode_name)
        synced_watcher.on_created(dir_1)

        # Assert
        self.assertListEqual(synced_watcher.created_paths, [dir_1])

        # Create file 1
        file_1 = self._createSourceFile(f'{episode_name}/RARBG_DO_NOT_MIRROR.exe')
        synced_watcher.on_created(file_1)

        # Assert
        self.assertListEqual(synced_watcher.created_paths, [dir_1])

        # Modify dir
        synced_watcher.on_modified(dir_1)

        # Assert
        self.assertListEqual(synced_watcher.created_paths, [dir_1])
        self.assertListEqual(synced_watcher.modified_paths, [dir_1])

        # Create file 2
        file_2 = self._createSourceFile(f'{episode_name}/{episode_name}-mytv.mkv')
        synced_watcher.on_created(file_2)

        # Assert
        self.assertListEqual(synced_watcher.created_paths, [dir_1])
        self.assertListEqual(synced_watcher.modified_paths, [dir_1])

        # Modify dir
        synced_watcher.on_modified(dir_1)

        # Assert
        self.assertListEqual(synced_watcher.created_paths, [dir_1])
        self.assertListEqual(synced_watcher.modified_paths, [dir_1])

        # Create file 3
        file_3 = self._createSourceFile(f'{episode_name}/RARBG.txt')
        synced_watcher.on_created(file_3)

        # Assert
        self.assertListEqual(synced_watcher.created_paths, [dir_1])
        self.assertListEqual(synced_watcher.modified_paths, [dir_1])

        # Modify dir
        synced_watcher.on_modified(dir_1)

        # Assert
        self.assertListEqual(synced_watcher.created_paths, [dir_1])
        self.assertListEqual(synced_watcher.modified_paths, [dir_1])

        # Modify file 3
        synced_watcher.on_modified(file_2)
        synced_watcher.on_modified(file_2)
        synced_watcher.on_modified(file_2)

        # Assert
        self.assertListEqual(synced_watcher.created_paths, [dir_1])
        self.assertListEqual(synced_watcher.modified_paths, [dir_1])
