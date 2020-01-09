import asyncio
import sys
import os
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from memover import arguments_parser, mover


class __Watcher:

    modified_files_dir_queue = []
    top_level_created_files_dir_queue = []
    start_time = time.time()

    def get_monitor_dir_path(self):
        args = arguments_parser.get_args()
        return args.source

    def auto_turn_off(self):
        args = arguments_parser.get_args()
        return args.quit

    async def print_queues_content(self):
        while True:
            print(f'modified_files_dir_queue: {self.modified_files_dir_queue}')
            print(f'top_level_created_files_dir_queue: {self.top_level_created_files_dir_queue}')
            await asyncio.sleep(3600)  # once an hour

    async def move_created_files(self):
        while True:
            if not self.top_level_created_files_dir_queue:
                await asyncio.sleep(1)
                continue
            dir_or_file = self.top_level_created_files_dir_queue[0]
            await self.move_created_when_ready(dir_or_file)

    async def move_created_when_ready(self, path):
        await asyncio.sleep(1)  # 1 second
        if path in self.modified_files_dir_queue:
            self.modified_files_dir_queue.remove(path)
            return await self.move_created_when_ready(path)

        print(f"Moving path {path}")
        self.move_file(path)
        del self.top_level_created_files_dir_queue[0]

    def move_file(self, path):
        args = arguments_parser.get_args()

        mover.move_media_by_path(
            path,
            args.show_destination,
            args.movie_destination
        )

    def queuepath_from_path(self, target_list, path):
        for target_list_path in target_list:
            if os.path.isdir(target_list_path):
                if target_list_path.replace(self.get_monitor_dir_path(), '') in path.replace(self.get_monitor_dir_path(), ''):  # inbox path is not valid
                    return target_list_path

        return path

    def path_in_queue(self, target_list, path):
        for target_list_path in target_list:
            if os.path.isdir(target_list_path):
                if target_list_path.replace(self.get_monitor_dir_path(), '') in path.replace(self.get_monitor_dir_path(), ''):  # inbox path is not valid
                    return True
            else: # If file
                if target_list_path == path:
                    return True

        return False

    def on_created(self, event):
        # print(f"event_type {event.event_type}")
        # print(f"os stat: {os.stat(event.src_path)}")
        print(f"{event.src_path} has been created")
        if self.path_in_queue(self.top_level_created_files_dir_queue, event.src_path):
            return

        self.top_level_created_files_dir_queue.append(event.src_path)

    def on_deleted(self, event):
        pass
        # print(f"{event.src_path} has been deleted!")

    def on_modified(self, event):
        # print(f"os stat: {repr(os.stat(event.src_path))}")
        # print(f"{event.src_path} has been modified")
        if event.src_path == self.get_monitor_dir_path():
            return

        if not os.path.exists(event.src_path):
            return

        # File is not in created files/dir queue
        if not self.path_in_queue(self.top_level_created_files_dir_queue, event.src_path):
            return

        # File is already in modified files/dir queue
        if self.path_in_queue(self.modified_files_dir_queue, event.src_path):
            return

        modified_path = self.queuepath_from_path(self.top_level_created_files_dir_queue, event.src_path)
        self.modified_files_dir_queue.append(modified_path)

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
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()

    async def auto_turn_off_handler(self):
        if not self.auto_turn_off():
            return

        while True:
            if time.time() > self.start_time + float(self.auto_turn_off()):
                sys.exit()
            await asyncio.sleep(1)


async def main():
    my_watcher = __Watcher()
    await asyncio.gather(
        my_watcher.observe(),
        my_watcher.move_created_files(),
        my_watcher.print_queues_content(),
        my_watcher.auto_turn_off_handler()
    )
