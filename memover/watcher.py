import asyncio
import sys
import os
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from memover import mover
from memover.arguments_parser import MeMoverArgs


class SyncedWatcher:

    def __init__(self):
        self.__modified_files_dir_queue = []
        self.__created_paths_to_move = []

    def print_state(self):
        print(f'modified_files_dir_queue: {self.__modified_files_dir_queue}')
        print(f'top_level_created_files_dir_queue: {self.__created_paths_to_move}')

    # Created_paths_to_move

    @property
    def modified_files_dir_queue(self):
        return self.__modified_files_dir_queue

    @property
    def created_paths_to_move(self):
        return self.__created_paths_to_move

    def no_created_files_to_move(self):
        return not self.__created_paths_to_move

    def pop_path_to_move(self):
        first_path_to_move = self.__created_paths_to_move[0]
        del self.__created_paths_to_move[0]
        return first_path_to_move

    def add_path_to_move(self, path):
        return self.__created_paths_to_move.append(path)

    def in_paths_to_move(self, path, monitor_path):
        return self.__path_in_queue(self.__created_paths_to_move, path, monitor_path)

    # Modified_paths

    def add_to_modified_paths(self, path, monitor_path):
        modified_path = self.queuepath_from_path(self.__created_paths_to_move, path, monitor_path)
        self.__modified_files_dir_queue.append(modified_path)

    def remove_path_from_modified_paths(self, path):
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


class Watcher:

    def __init__(self, args: MeMoverArgs) -> None:
        self.__start_time = time.time()
        self.__args = args
        self.__synced_watcher = SyncedWatcher()

    @property
    def modified_files_dir_queue(self):
        return self.__synced_watcher.modified_files_dir_queue

    @property
    def created_paths_to_move(self):
        return self.__synced_watcher.created_paths_to_move

    def get_monitor_dir_path(self):
        return self.__args.source

    def auto_turn_off(self):
        return self.__args.quit

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
        await asyncio.sleep(1)  # 1 second
        if self.__synced_watcher.in_modified_files(path, self.get_monitor_dir_path()):
            self.__synced_watcher.remove_path_from_modified_paths(path)
            return await self.move_created_when_ready(path)

        print(f"Moving path {path}")
        self.move_file(path)

    def move_file(self, path):
        mover.move_media_by_path(
            path,
            self.__args.show_destination,
            self.__args.movie_destination
        )

    def on_created(self, event):
        # print(f"event_type {event.event_type}")
        # print(f"os stat: {os.stat(event.src_path)}")
        print(f"{event.src_path} has been created")
        if self.__synced_watcher.in_paths_to_move(event.src_path, self.get_monitor_dir_path()):
            return

        self.__synced_watcher.add_path_to_move(event.src_path)

    def on_deleted(self, event):
        pass
        # print(f"{event.src_path} has been deleted!")

    def on_modified(self, event):
        print(f"os stat: {repr(os.stat(event.src_path))}")
        print(f"{event.src_path} has been modified")

        if event.src_path.strip('/') == self.get_monitor_dir_path().strip('/'):
            return

        if not os.path.exists(event.src_path):
            return

        # File is already in modified files/dir queue
        if self.__synced_watcher.in_modified_files(event.src_path, self.get_monitor_dir_path()):
            return

        self.__synced_watcher.add_to_modified_paths(event.src_path, self.get_monitor_dir_path())

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

        path = self.get_monitor_dir_path()
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
        return self.auto_turn_off() and (time.time() > self.__start_time + float(self.auto_turn_off()))


async def run(args: MeMoverArgs):
    my_watcher = Watcher(args)
    await asyncio.gather(
        my_watcher.observe(),
        my_watcher.move_created_files(),
        my_watcher.print_queues_content()
    )
