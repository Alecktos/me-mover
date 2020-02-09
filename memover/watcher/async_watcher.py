import asyncio
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from memover import logger
from memover.arguments_parser import MeMoverArgs
from memover.watcher.synced_watcher import SyncedWatcher


class AsyncWatcher:

    def __init__(self, args: MeMoverArgs) -> None:
        self.__start_time = time.time()
        self.__args = args
        self.__synced_watcher = SyncedWatcher(args)

    @property
    def modified_paths(self):
        return self.__synced_watcher.modified_paths

    @property
    def created_paths(self):
        return self.__synced_watcher.created_paths

    async def move_created_files(self):
        while not self.should_quit():
            self.__synced_watcher.move_next_path()
            await asyncio.sleep(1)  # 1 second

    def on_created(self, event):
        self.__synced_watcher.on_created(event.src_path)

    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        self.__synced_watcher.on_modified(event.src_path)

    def on_moved(event):
        pass

    async def observe(self):
        patterns = "*"
        ignore_patterns = ""
        ignore_directories = False
        case_sensitive = True

        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_created = self.on_created
        my_event_handler.on_deleted = self.on_deleted
        my_event_handler.on_modified = self.on_modified
        my_event_handler.on_moved = self.on_moved

        path = self.__args.source
        logger.info(f"Watching: {path}")
        go_recursively = True
        my_observer = Observer()
        my_observer.schedule(my_event_handler, path, recursive=go_recursively)
        my_observer.start()

        try:
            while not self.should_quit():
                await asyncio.sleep(1)
        finally:
            my_observer.stop()
            my_observer.join()

    def should_quit(self):
        return self.__args.quit and (time.time() > self.__start_time + float(self.__args.quit))


async def run(args: MeMoverArgs):
    my_watcher = AsyncWatcher(args)
    await asyncio.gather(
        my_watcher.observe(),
        my_watcher.move_created_files()
    )
