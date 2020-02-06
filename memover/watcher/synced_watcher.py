import os

from memover import mover


class SyncedWatcher:

    def __init__(self):
        self.__modified_files_dir_queue = []
        self.__created_paths_to_move = []

    def print_state(self):
        print(f'modified_files_dir_queue: {self.__modified_files_dir_queue}')
        print(f'top_level_created_files_dir_queue: {self.__created_paths_to_move}')

    def move_file(self, path, show_destination, movie_destination):
        mover.move_media_by_path(
            path,
            show_destination,
            movie_destination
        )

    # Created_paths_to_move

    @property
    def created_paths_to_move(self):
        return self.__created_paths_to_move

    def no_created_files_to_move(self):
        return not self.__created_paths_to_move

    def pop_path_to_move(self):
        first_path_to_move = self.__created_paths_to_move[0]
        del self.__created_paths_to_move[0]
        return first_path_to_move

    def add_path_to_move(self, path, monitor_path):
        print(f"{path} has been created")
        if self.in_paths_to_move(path, monitor_path):
            return
        return self.__created_paths_to_move.append(path)

    def in_paths_to_move(self, path, monitor_path):
        return self.__path_in_queue(self.__created_paths_to_move, path, monitor_path)

    # Modified_paths

    @property
    def modified_files_dir_queue(self):
        return self.__modified_files_dir_queue

    def add_to_modified_paths(self, path, monitor_path):
        if path.strip('/') == monitor_path.strip('/'):
            return

        if not os.path.exists(path):
            print(f"modified file path does not exist anymore: {path}")
            return

        # File is already in modified files/dir queue
        if self.in_modified_files(path, monitor_path):
            print(f'file is already in modified file queue {path}')
            return

        modified_path = self.queuepath_from_path(self.__created_paths_to_move, path, monitor_path)
        self.__modified_files_dir_queue.append(modified_path)

    def remove_path_from_modified_paths(self, path):
        print(f"Removed from modified path {path}")
        self.__modified_files_dir_queue.remove(path)

    def in_modified_files(self, path, monitor_path):
        return self.__path_in_queue(self.__modified_files_dir_queue, path, monitor_path)

    # Utils

    def __path_in_queue(self, target_list, path, monitor_path):
        normalized_path = path.strip('/')
        for target_list_path in target_list:
            normalized_target_list_path = target_list_path.strip('/')
            if os.path.isdir(target_list_path):
                if target_list_path.replace(monitor_path, '') in path.replace(monitor_path, ''):  # inbox path is not valid
                    return True
            else: # If file
                if normalized_target_list_path == normalized_path:
                    return True

        return False

    def queuepath_from_path(self, target_list, path, monitor_path):
        for target_list_path in target_list:
            if os.path.isdir(target_list_path):
                if target_list_path.replace(monitor_path, '') in path.replace(monitor_path, ''):  # inbox path is not valid
                    return target_list_path

        return path
