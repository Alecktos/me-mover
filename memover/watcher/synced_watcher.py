import os

from memover import mover, logger
from memover.arguments_parser import MeMoverArgs


class SyncedWatcher:

    def __init__(self, args: MeMoverArgs):
        self.__modified_paths = []
        self.__created_paths = []
        self.__args = args

    def move_next_path(self):
        if not self.__created_paths:
            return False

        path = self.__created_paths[0]

        if self.__in_modified_files(path):
            self.__modified_paths.remove(path)
            return False

        # Remove file from queue before moving to avoid changes to file in modify queue
        del self.__created_paths[0]

        logger.debug(f'modified_paths queue before move: {self.__modified_paths}')
        logger.debug(f'created_paths queue before move: {self.__created_paths}')
        mover.move_media_by_path(
            path,
            self.__args.show_destination,
            self.__args.movie_destination
        )
        logger.debug(f'modified_paths queue after move: {self.__modified_paths}')
        logger.debug(f'created_paths queue after move: {self.__created_paths}')
        return True

    # Created_paths_to_move

    @property
    def created_paths(self):
        return self.__created_paths

    def on_created(self, path):
        if self.__in_create_files(path):
            return
        return self.__created_paths.append(path)

    def __in_create_files(self, path):
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

        if not self.__in_create_files(path):
            return

        # File is already in modified files/dir queue
        if self.__in_modified_files(path):
            return

        modified_path = self.__queuepath_from_path(self.__created_paths, path)
        self.__modified_paths.append(modified_path)

    def __in_modified_files(self, path):
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
