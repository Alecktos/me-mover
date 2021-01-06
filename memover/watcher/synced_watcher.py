import os

from memover import mover, logger
from memover.arguments_parser import MeMoverArgs
from memover.watcher.path_queue import PathQueue


class SyncedWatcher:

    def __init__(self, args: MeMoverArgs):
        self.__modified_paths_queue = PathQueue(args)
        self.__created_paths_queue = PathQueue(args)
        self.__args = args

    def move_next_path(self):
        if self.__created_paths_queue.is_empty():
            return False

        path = self.__created_paths_queue.next()

        if self.__modified_paths_queue.in_queue(path):
            self.__modified_paths_queue.remove(path)
            return False

        self.__log_queue_status('Queues Before Move: Before removing path')

        # Remove file from queue before moving to avoid changes to file in modify queue
        self.__created_paths_queue.remove(path)

        self.__log_queue_status('Queues Before Move: after removing path')
        mover.move_media_by_path(
            path,
            self.__args.show_destination,
            self.__args.movie_destination
        )
        self.__log_queue_status('Queues After Move')
        return True

    def __log_queue_status(self, header):
        logger.debug(f'-- {header} --')
        self.__modified_paths_queue.log_debug('modified_paths')
        self.__created_paths_queue.log_debug('created_paths')
        logger.debug('-- End --')

    # Created_paths_to_move

    @property
    def created_paths(self):
        return self.__created_paths_queue

    def on_created(self, path):
        self.__created_paths_queue.append(path)
        self.on_modified(path)

    # Modified_paths

    @property
    def modified_paths(self):
        return self.__modified_paths_queue

    def on_modified(self, path):
        if path.strip('/') == self.__args.source.strip('/'):
            return

        if not os.path.exists(path):
            return

        if not self.__created_paths_queue.in_queue(path):
            return

        self.__modified_paths_queue.append(path)
