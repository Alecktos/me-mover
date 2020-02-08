import unittest

from memover.arguments_parser import MeMoverArgs, Commands
from memover.watcher.synced_watcher import SyncedWatcher
from tests.utils import file_mover_tester


class TestSyncedWatcher(unittest.TestCase, file_mover_tester.FileMoverTester):

    __episode_name = 'kolla.S04E15.asswe.xTTT-RR[abf]'
    __synced_watcher = None

    def setUp(self):
        self._create_test_dirs()
        args = MeMoverArgs(
            Commands.WATCH,
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )
        self.__synced_watcher = SyncedWatcher(args)

    def tearDown(self):
        self._delete_test_dirs()

    def test_only_root_added_queues(self):
        # Create dir
        dir_1 = self._create_source_dir(self.__episode_name)
        self.__synced_watcher.on_created(dir_1)

        # Assert
        self.assertListEqual(self.__synced_watcher.created_paths, [dir_1])

        # Create file 1
        file_1_data = self.__create_file_and_trigger_created('DO_NOT_MIRROR.exe')

        # Assert
        self.assertListEqual(self.__synced_watcher.created_paths, [dir_1])

        # Modify dir
        self.__synced_watcher.on_modified(dir_1)

        # Assert
        self.assertListEqual(self.__synced_watcher.created_paths, [dir_1])
        self.assertListEqual(self.__synced_watcher.modified_paths, [dir_1])

        # Create file 2
        file_2_data = self.__create_file_and_trigger_created(f'{self.__episode_name}-mytv.mkv')

        # Assert
        self.assertListEqual(self.__synced_watcher.created_paths, [dir_1])
        self.assertListEqual(self.__synced_watcher.modified_paths, [dir_1])

        # Modify dir
        self.__synced_watcher.on_modified(dir_1)

        # Assert
        self.assertListEqual(self.__synced_watcher.created_paths, [dir_1])
        self.assertListEqual(self.__synced_watcher.modified_paths, [dir_1])

        # Create file 3
        file_3_data = self.__create_file_and_trigger_created('Gamma.txt')

        # Assert
        self.assertListEqual(self.__synced_watcher.created_paths, [dir_1])
        self.assertListEqual(self.__synced_watcher.modified_paths, [dir_1])

        # Modify dir
        self.__synced_watcher.on_modified(dir_1)

        # Assert
        self.assertListEqual(self.__synced_watcher.created_paths, [dir_1])
        self.assertListEqual(self.__synced_watcher.modified_paths, [dir_1])

        # Modify file 2
        self.__synced_watcher.on_modified(file_2_data['path'])
        self.__synced_watcher.on_modified(file_2_data['path'])
        self.__synced_watcher.on_modified(file_2_data['path'])

        # Assert
        self.assertListEqual(self.__synced_watcher.created_paths, [dir_1])
        self.assertListEqual(self.__synced_watcher.modified_paths, [dir_1])

        # Try to move
        self.__synced_watcher.move_next_path()

        # Assert
        self.assertListEqual(self.__synced_watcher.created_paths, [dir_1])
        self.assertListEqual(self.__synced_watcher.modified_paths, [])

        # Actually moving
        self.__synced_watcher.move_next_path()

        # Assert Moved
        self.assert_moved(file_3_data)
        self.assert_moved(file_2_data)
        self.assert_moved(file_1_data)

    def __create_file_and_trigger_created(self, file):
        relative_path = f'{self.__episode_name}/{file}'
        path = self._createSourceFile(relative_path)
        self.__synced_watcher.on_created(path)
        return {
            'relative_path': relative_path,
            'path': path,
            'file': file
        }

    def assert_moved(self, file_data):
        self._assert_file_moved(
            file_data['relative_path'],
            f'{self._SHOW_DESTINATION_DIRECTORY}/kolla/Season 4/{file_data["file"]}'
        )

