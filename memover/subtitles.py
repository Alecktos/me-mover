from memover import file_handler, logger


class _BiggestFile:
    def __init__(self):
        self.size = -1
        self.path = None


def rename_and_move(source_directory):
    if not file_handler.path_is_directory(source_directory):
        return

    subtitle_files = []
    biggest_file = _BiggestFile()  # assuming that the media file is the biggest file we can found.

    for file_path in file_handler.get_files(source_directory):
        file_size = file_handler.get_file_size(file_path)
        if file_size > biggest_file.size:
            biggest_file.size = file_size
            biggest_file.path = file_path

        if file_path.endswith(('.srt', '.smi', '.ssa', '.ass', '.vtt')):
            subtitle_files.append(file_path)

    if not biggest_file.path:
        raise NoMediaFileException('Could not find media file when renaming subtitle. Source directory: '
                                   + source_directory)

    media_file_excluded_extension = file_handler.get_path_without_extension(biggest_file.path)
    for index, subtitle_path in enumerate(subtitle_files):
        rename_file(subtitle_path, media_file_excluded_extension, index)
        __delete_parents_directory_parents(subtitle_path)


def rename_file(subtitle_source_path, media_file_path_without_extension, index):
    subtitle_type = file_handler.get_file_type(subtitle_source_path)
    index_name = '' if index == 0 else str(index + 1)

    # assuming all subs are english for now
    file_handler.move_file(
        subtitle_source_path,
        media_file_path_without_extension + '.en' + index_name + subtitle_type
    )


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


class NoMediaFileException(Exception):
    def __init__(self, message):
        super(NoMediaFileException, self).__init__(message)