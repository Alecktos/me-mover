import time
from dataclasses import dataclass
from typing import Optional

from memover import logger
from memover.arguments_parser import MeMoverArgs


@dataclass
class QueueItem:
    path: str
    last_modified: float
    modified: bool


class PathQueue:

    def __init__(self, args: MeMoverArgs):
        self.__queue = []
        self.__args = args

    def __eq__(self, other):
        if isinstance(other, list):
            return [item.path for item in self.__queue] == other
        return self is other

    def __repr__(self):
        return str([item.path for item in self.__queue])

    def is_empty(self):
        return not self.__queue

    def next(self) -> QueueItem:
        return self.__queue[0]

    def remove(self, path):
        cleaned_path = self.__clean_path(path)
        for item in self.__queue:
            if item.path == cleaned_path:
                self.__queue.remove(item)
                return

    def append(self, path, timestamp: float):
        cleaned_path = self.__clean_path(path)
        if self.in_queue(path):
            return
        self.__queue.append(QueueItem(path=cleaned_path, last_modified=timestamp, modified=True))

    def log_debug(self, queue_name):
        logger.debug(f'{queue_name}: {[item.path for item in self.__queue]}')

    def in_queue(self, path):
        cleaned_path = self.__clean_path(path)
        for item in self.__queue:
            if item.path == cleaned_path:
                return True
        return False

    def update_last_modified(self, path, timestamp: float):
        cleaned_path = self.__clean_path(path)
        for item in self.__queue:
            if item.path == cleaned_path:
                item.last_modified = timestamp
                item.modified = True
                return

    def get_last_modified(self, path) -> Optional[float]:
        cleaned_path = self.__clean_path(path)
        for item in self.__queue:
            if item.path == cleaned_path:
                return item.last_modified
        return None

    def time_since_last_modified(self, path, current_time: float = None) -> Optional[float]:
        if current_time is None:
            current_time = time.time()
        timestamp = self.get_last_modified(path)
        if timestamp is None:
            return None
        return current_time - timestamp

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
