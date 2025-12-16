import os
import time

from memover import mover, logger
from memover.arguments_parser import MeMoverArgs
from memover.watcher.path_queue import PathQueue
from pathlib import Path


class SyncedWatcher:
    # Number of seconds a file must be stable (no modifications) before moving
    DEFAULT_STABLE_SECONDS = 5

    def __init__(self, args: MeMoverArgs, stable_seconds: float = None):
        self.__created_paths_queue = PathQueue(args)
        self.__args = args
        self.__stable_seconds = stable_seconds if stable_seconds is not None else self.DEFAULT_STABLE_SECONDS

    def move_next_path(self):
        if self.__created_paths_queue.is_empty():
            return False

        queue_item = self.__created_paths_queue.next()

        # First check: if file is in modified,set it to false and wait for next cycle
        if queue_item.modified:
            queue_item.modified = False
            logger.debug(f'File {queue_item.path} was modified recently, waiting for next cycle')
            return False

        # Second check: ensure file was stable for stable_seconds after last modification
        time_since_last_modify = self.__created_paths_queue.time_since_last_modified(queue_item.path)
        if time_since_last_modify is not None and time_since_last_modify < self.__stable_seconds:
            logger.debug(f'File {queue_item.path} was modified {time_since_last_modify:.1f}s ago, waiting for {self.__stable_seconds}s of stability')
            return False

        self.__log_queue_status('Queues Before Move: Before removing path')

        self.__created_paths_queue.remove(queue_item.path)

        self.__log_queue_status('Queues Before Move: after removing path')
        mover.move_media_by_path(
            queue_item.path,
            self.__args.show_destination,
            self.__args.movie_destination
        )
        self.__log_queue_status('Queues After Move')

        return True

    def __log_queue_status(self, header):
        logger.debug(f'-- {header} --')
        self.__created_paths_queue.log_debug('created_paths')
        logger.debug('-- End --')

    def __is_source_dir(self, path):
        return path.strip('/') == self.__args.source.strip('/') or Path(self.__args.source).parent == Path(path)

    @property
    def created_paths(self):
        return self.__created_paths_queue

    def on_created(self, path):
        if self.__is_source_dir(path):
            return

        if not os.path.exists(path):
            logger.debug(f'FileCreated event for path {path} that does not exist')
            return

        self.__created_paths_queue.append(path, time.time())

        self.on_modified(path)

    def on_modified(self, path):
        if self.__is_source_dir(path):
            return

        if not os.path.exists(path):
            return

        if not self.__created_paths_queue.in_queue(path):
            return

        # Track the time of this modification
        current_time = time.time()
        self.__created_paths_queue.update_last_modified(path, current_time)
