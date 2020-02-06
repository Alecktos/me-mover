import asyncio
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from memover.arguments_parser import MeMoverArgs
from memover.watcher.synced_watcher import SyncedWatcher


class AsyncWatcher:

    def __init__(self, args: MeMoverArgs) -> None:
        self.__start_time = time.time()
        self.__args = args
        self.__synced_watcher = SyncedWatcher(args)

    @property
    def modified_files_dir_queue(self):
        return self.__synced_watcher.modified_files_dir_queue

    @property
    def created_paths_to_move(self):
        return self.__synced_watcher.created_paths_to_move

    async def print_queues_content(self):
        if not self.should_quit():   # Dont run when auto quit is on
            return
        self.__synced_watcher.print_state()
        await asyncio.sleep(3600)  # once an hour

    async def move_created_files(self):
        while not self.should_quit():
            if self.__synced_watcher.no_created_files_to_move():
                await asyncio.sleep(1)
                continue
            dir_or_file = self.__synced_watcher.pop_path_to_move()
            await self.move_created_when_ready(dir_or_file)

    async def move_created_when_ready(self, path):
        while self.__synced_watcher.move_file(path) is False:
            await asyncio.sleep(2)  # 1 second

    def on_created(self, event):
        # print(f"event_type {event.event_type}")
        # print(f"os stat: {os.stat(event.src_path)}")
        self.__synced_watcher.add_path_to_move(event.src_path)

    def on_deleted(self, event):
        pass
        # print(f"{event.src_path} has been deleted!")

    def on_modified(self, event):
        self.__synced_watcher.add_to_modified_paths(event.src_path)

    def on_moved(event):
        # print(f"{event.src_path} has been moved!")
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
        print(f"Listening on path: {path}")
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
        my_watcher.move_created_files(),
        my_watcher.print_queues_content()
    )
