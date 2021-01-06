import os

from memover import logger
from memover.arguments_parser import MeMoverArgs


class PathQueue:

    def __init__(self, args: MeMoverArgs):
        self.__queue = []
        self.__args = args

    def __eq__(self, other):
        if isinstance(other, list):
            return self.__queue == other
        return self is other

    def is_empty(self):
        return not self.__queue

    def next(self):
        return self.__queue[0]

    def remove(self, path):
        self.__queue.remove(path)

    def append(self, path):
        self.__queue.append(path)

    def log_debug(self, queue_name):
        logger.debug(f'{queue_name}: {self.__queue}')

    def in_queue(self, path):
        for target_list_path in self.__queue:
            if os.path.isdir(target_list_path):
                if target_list_path.replace(self.__args.source, '') in path.replace(self.__args.source, ''):  # inbox path is not valid
                    return True
            else:  # If file
                if target_list_path == path:
                    return True

        return False

    def queue_path_from_path(self, path):
        for target_list_path in self.__queue:
            if os.path.isdir(target_list_path):
                if target_list_path.replace(self.__args.source, '') in path.replace(self.__args.source, ''):  # inbox path is not valid
                    return target_list_path
        return path