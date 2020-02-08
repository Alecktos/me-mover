import os

from memover import mover
from memover.arguments_parser import MeMoverArgs


class SyncedWatcher:

    def __init__(self, args: MeMoverArgs):
        self.__modified_files_dir_queue = []
        self.__created_paths_to_move = []
        self.__args = args

    def print_state(self):
        print(f'modified_files_dir_queue: {self.__modified_files_dir_queue}')
        print(f'top_level_created_files_dir_queue: {self.__created_paths_to_move}')

    def move_next_path(self):
        if not self.__created_paths_to_move:
            return

        path = self.__created_paths_to_move[0]

        if self.__in_modified_files(path, self.__args.source):
            self.__remove_path_from_modified_paths(path)
            return

        print(f"Moving path {path}")
        mover.move_media_by_path(
            path,
            self.__args.show_destination,
            self.__args.movie_destination
        )

        # Remove file from queue when moved
        del self.__created_paths_to_move[0]

    # Created_paths_to_move

    @property
    def created_paths_to_move(self):
        return self.__created_paths_to_move

    def on_created(self, path):
        print(f"{path} has been created")
        if self.in_paths_to_move(path, self.__args.source):
            return
        return self.__created_paths_to_move.append(path)

    def in_paths_to_move(self, path, monitor_path):
        return self.__path_in_queue(self.__created_paths_to_move, path)

    # Modified_paths

    @property
    def modified_files_dir_queue(self):
        return self.__modified_files_dir_queue

    def on_modified(self, path):
        if path.strip('/') == self.__args.source.strip('/'):
            return

        if not os.path.exists(path):
            print(f"modified file path does not exist anymore: {path}")
            return

        # File is already in modified files/dir queue
        if self.__in_modified_files(path, self.__args.source):
            print(f'file is already in modified file queue {path}')
            return

        modified_path = self.__queuepath_from_path(self.__created_paths_to_move, path)
        self.__modified_files_dir_queue.append(modified_path)

    def __remove_path_from_modified_paths(self, path):
        print(f"Removed from modified path {path}")
        self.__modified_files_dir_queue.remove(path)

    def __in_modified_files(self, path, monitor_path):
        return self.__path_in_queue(self.__modified_files_dir_queue, path)

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
