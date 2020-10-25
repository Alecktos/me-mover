import asyncio
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from memover import logger
from memover.arguments_parser import MeMoverArgs
from memover.watcher.synced_watcher import SyncedWatcher


class AsyncWatcher:

    SLEEP_SECONDS = 2

    def __init__(self, args: MeMoverArgs) -> None:
        self.__start_time = time.time()
        self.__args = args
        self.__synced_watcher = SyncedWatcher(args)
        self.__moves = 0

    @property
    def modified_paths(self):
        return self.__synced_watcher.modified_paths

    @property
    def created_paths(self):
        return self.__synced_watcher.created_paths

    def move_created_files(self):
        success = self.__synced_watcher.move_next_path()
        if success:
            self.__moves += 1

    def on_created(self, event):
        self.__synced_watcher.on_created(event.src_path)

    def on_modified(self, event):
        self.__synced_watcher.on_modified(event.src_path)

    async def observe(self):
        patterns = "*"
        ignore_patterns = ""
        ignore_directories = False
        case_sensitive = True

        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_created = self.on_created
        my_event_handler.on_modified = self.on_modified

        path = self.__args.source
        logger.info(f"Watching: {path}")
        go_recursively = True
        my_observer = Observer()
        my_observer.schedule(my_event_handler, path, recursive=go_recursively)
        my_observer.start()

        try:
            while not self.should_quit():
                self.move_created_files()
                await asyncio.sleep(self.SLEEP_SECONDS)
        finally:
            my_observer.stop()
            my_observer.join()

    def should_quit(self):
        if self.__args.moves_before_quit and self.__moves >= self.__args.moves_before_quit:
            return True

        return False


async def run(args: MeMoverArgs):
    my_watcher = AsyncWatcher(args)
    await asyncio.gather(
        my_watcher.observe()
    )
