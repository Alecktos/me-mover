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
        cleaned_path = self.__clean_path(path)
        if cleaned_path in self.__queue:
            return
        self.__queue.append(cleaned_path)

    def log_debug(self, queue_name):
        logger.debug(f'{queue_name}: {self.__queue}')

    def in_queue(self, path):
        path = self.__clean_path(path)
        for queue_path in self.__queue:
            if queue_path == path:
                return True
        return False

    def __clean_path(self, path):
        everything_after_source = self.__lstrip_source(path)
        everything_after_source = everything_after_source.lstrip('/')

        try:
            slash_index = everything_after_source.index('/')
            first_root_path = everything_after_source[:slash_index]
        except ValueError:
            first_root_path = everything_after_source

        first_root_path = first_root_path.rstrip('/')
        source = self.__args.source.rstrip('/')
        return f'{source}/{first_root_path}'

    def __lstrip_source(self, path):
        index = path.index(self.__args.source) + len(self.__args.source)
        return path[index:]
