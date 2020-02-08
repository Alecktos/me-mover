import os

from memover import mover
from memover.arguments_parser import MeMoverArgs


class SyncedWatcher:

    def __init__(self, args: MeMoverArgs):
        self.__modified_paths = []
        self.__created_paths = []
        self.__args = args

    def print_state(self):
        print(f'modified_files_dir_queue: {self.__modified_paths}')
        print(f'top_level_created_files_dir_queue: {self.__created_paths}')

    def move_next_path(self):
        if not self.__created_paths:
            return

        path = self.__created_paths[0]

        if self.__in_modified_files(path, self.__args.source):
            self.__modified_paths.remove(path)
            return

        print(f"Moving path {path}")
        mover.move_media_by_path(
            path,
            self.__args.show_destination,
            self.__args.movie_destination
        )

        # Remove file from queue when moved
        del self.__created_paths[0]

    # Created_paths_to_move

    @property
    def created_paths(self):
        return self.__created_paths

    def on_created(self, path):
        print(f"{path} has been created")
        if self.__in_paths_to_move(path, self.__args.source):
            return
        return self.__created_paths.append(path)

    def __in_paths_to_move(self, path, monitor_path):
        return self.__path_in_queue(self.__created_paths, path)

    # Modified_paths

    @property
    def modified_paths(self):
        return self.__modified_paths

    def on_modified(self, path):
        if path.strip('/') == self.__args.source.strip('/'):
            return

        if not os.path.exists(path):
            return

        # File is already in modified files/dir queue
        if self.__in_modified_files(path, self.__args.source):
            return

        modified_path = self.__queuepath_from_path(self.__created_paths, path)
        self.__modified_paths.append(modified_path)

    def __in_modified_files(self, path, monitor_path):
        return self.__path_in_queue(self.__modified_paths, path)

    # Utils

    def __path_in_queue(self, target_list, path):
        for target_list_path in target_list:
            if os.path.isdir(target_list_path):
                if target_list_path.replace(self.__args.source, '') in path.replace(self.__args.source, ''):  # inbox path is not valid
                    return True
            else:  # If file
                if target_list_path == path:
                    return True

        return False

    def __queuepath_from_path(self, target_list, path):
        for target_list_path in target_list:
            if os.path.isdir(target_list_path):
                if target_list_path.replace(self.__args.source, '') in path.replace(self.__args.source, ''):  # inbox path is not valid
                    return target_list_path

        return path
