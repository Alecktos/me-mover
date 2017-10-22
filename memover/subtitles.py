from memover import file_handler


class _BiggestFile:
    def __init__(self):
        self.size = 0
        self.path = None


def rename_and_move(source_directory):
    subtitle_files = []
    biggest_file = _BiggestFile()

    for file_path in file_handler.get_files(source_directory):
        file_size = file_handler.get_file_size(file_path)
        if file_size > biggest_file.size:
            biggest_file.size = file_size
            biggest_file.path = file_path

        if file_path.endswith(('.srt', '.smi', '.ssa', '.ass', '.vtt')):
            subtitle_files.append(file_path)

    for subtitle_path in subtitle_files:
        subtitle_type = file_handler.get_file_type(subtitle_path)
        file_handler.move_file(
            subtitle_path,
            file_handler.get_path_without_extension(biggest_file.path) + subtitle_type
        )

        __delete_parents_directory_parents(subtitle_path)


def __delete_parents_directory_parents(path):
    if not file_handler.path_is_directory(path):
        path = file_handler.get_parent(path)

    if file_handler.directory_is_empty(path):
        file_handler.delete_directory(path)

    path = file_handler.get_parent(path)
    if not path:
        return

    if file_handler.directory_is_empty(path):
        __delete_parents_directory_parents(path)

