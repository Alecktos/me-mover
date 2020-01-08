import asyncio
import sys
import os
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from memover import arguments_parser_2, mover

modified_files_dir_queue = []
top_level_created_files_dir_queue = []
start_time = time.time()


def get_monitor_dir_path():
    args = arguments_parser_2.get_args()
    return args.source


def auto_turn_off():
    args = arguments_parser_2.get_args()
    return args.quit


async def print_queues_content():
    while True:
        print(f'modified_files_dir_queue: {modified_files_dir_queue}')
        print(f'top_level_created_files_dir_queue: {top_level_created_files_dir_queue}')
        await asyncio.sleep(3600)  # once an hour


async def move_created_files():
    while True:
        if not top_level_created_files_dir_queue:
            await asyncio.sleep(1)
            continue
        dir_or_file = top_level_created_files_dir_queue[0]
        await move_created_when_ready(dir_or_file)


async def move_created_when_ready(path):
    await asyncio.sleep(1)  # 1 second
    if path in modified_files_dir_queue:
        modified_files_dir_queue.remove(path)
        return await move_created_when_ready(path)

    print(f"Moving path {path}")
    move_file(path)
    del top_level_created_files_dir_queue[0]


def move_file(path):
    args = arguments_parser_2.get_args()

    mover.move_media_by_path(
        path,
        args.show_destination,
        args.movie_destination
    )


def queuepath_from_path(target_list, path):
    for target_list_path in target_list:
        if os.path.isdir(target_list_path):
            if target_list_path.replace(get_monitor_dir_path(), '') in path.replace(get_monitor_dir_path(), ''):  # inbox path is not valid
                return target_list_path

    return path


def path_in_queue(target_list, path):
    for target_list_path in target_list:
        if os.path.isdir(target_list_path):
            if target_list_path.replace(get_monitor_dir_path(), '') in path.replace(get_monitor_dir_path(), ''):  # inbox path is not valid
                return True
        else: # If file
            if target_list_path == path:
                return True

    return False


def on_created(event):
    # print(f"event_type {event.event_type}")
    # print(f"os stat: {os.stat(event.src_path)}")
    print(f"{event.src_path} has been created")
    if path_in_queue(top_level_created_files_dir_queue, event.src_path):
        return

    top_level_created_files_dir_queue.append(event.src_path)


def on_deleted(event):
    pass
    # print(f"{event.src_path} has been deleted!")


def on_modified(event):
    # print(f"os stat: {repr(os.stat(event.src_path))}")
    print(f"{event.src_path} has been modified")
    if event.src_path == get_monitor_dir_path():
        return

    if not os.path.exists(event.src_path):
        return

    # File is not in created files/dir queue
    if not path_in_queue(top_level_created_files_dir_queue, event.src_path):
        return

    # File is already in modified files/dir queue
    if path_in_queue(modified_files_dir_queue, event.src_path):
        return

    modified_path = queuepath_from_path(top_level_created_files_dir_queue, event.src_path)
    modified_files_dir_queue.append(modified_path)


def on_moved(event):
    # print(f"{event.src_path} has been moved!")
    pass


async def observe():
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True

    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = get_monitor_dir_path()
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


async def auto_turn_off_handler():
    if not auto_turn_off():
        return

    while True:
        print('auto turnoff: ' + str(auto_turn_off()))
        if time.time() > start_time + float(auto_turn_off()):
            print('a: ' + str(start_time + float(auto_turn_off())))
            print('b: ' + str(time.time()))
            print("Exiting because of auto stop")
            sys.exit()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(observe(), move_created_files(), print_queues_content(), auto_turn_off_handler())
