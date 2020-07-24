import re

from memover import file_handler, media_file_extractor, language_codes

__subtitle_types = ('.srt', '.smi', '.ssa', '.ass', '.vtt')


def rename_and_move(source_directory):
    if not file_handler.path_is_directory(source_directory):
        return

    files = list(file_handler.get_files(source_directory))

    files.sort(key=lambda f: file_handler.get_last_path_part(f))

    for file_path in files:
        if __should_be_moved(file_path):
            file_path = __move_subtitle(file_path, source_directory)
        if __should_be_renamed(file_path):
            __rename(file_path)


def __should_be_moved(subtitle_path):
    if not subtitle_path.endswith(__subtitle_types):
        return False

    subtitle_dir = file_handler.get_parent(subtitle_path)
    biggest_file = file_handler.get_biggest_file(subtitle_dir)
    if media_file_extractor.is_media_file(biggest_file.path):
        return False

    return True


def __should_be_renamed(subtitle_path):
    if not subtitle_path.endswith(__subtitle_types):
        return False

    subtitle_dir = file_handler.get_parent(subtitle_path)
    biggest_file = file_handler.get_biggest_file(subtitle_dir)
    if not media_file_extractor.is_media_file(biggest_file.path):
        return False # No media file. Nothing to rename to

    biggest_file_name = file_handler.get_last_path_part(biggest_file.path)
    subtitle_file_name = file_handler.get_last_path_part(subtitle_path)

    # should be moved if subtitle is not already named after media file in directory
    return subtitle_file_name.find(biggest_file_name) == -1


def __move_subtitle(subtitle_path, source_directory):
    for biggest_file in file_handler.get_biggest_files(file_handler.get_parent(subtitle_path), source_directory):
        if media_file_extractor.is_media_file(biggest_file.path):
            destination_path = file_handler.get_parent(biggest_file.path) + '/' + file_handler.get_last_path_part(subtitle_path)

            file_handler.move(
                subtitle_path,
                destination_path
            )
            __delete_empty_parents(subtitle_path, source_directory)
            return destination_path


def __rename(file_path):
    subtitle_type = file_handler.get_file_type(file_path)

    biggest_file = file_handler.get_biggest_file(file_handler.get_parent(file_path))
    if not media_file_extractor.is_media_file(biggest_file.path):
        return

    language_code = __identify_language(file_path)
    index = __calculate_index(language_code, file_path)

    destination_path = file_handler.get_path_without_extension(biggest_file.path) + '.' + language_code + index + subtitle_type

    file_handler.move(
        file_path,
        destination_path
    )


def __calculate_index(language_code, file_path):
    dir = file_handler.get_parent(file_path)
    files_in_dir = file_handler.get_directory_content(dir)
    files = [file for file in files_in_dir if re.search(r'\.' + language_code + r'\d*\.', file) is not None]
    index = len(files)
    return '' if index == 0 else str(index + 1)


def __identify_language(file_path):
    file = file_handler.get_last_path_part(file_path)
    by_code = language_codes.find_by_three_letter_code(file)
    if by_code:
        return by_code[1]

    by_language = language_codes.find_by_language(file)
    if by_language:
        return by_language[1]

    return 'en'  # Default to english if cant find a language in file name


def __delete_empty_parents(path, source_directory):
    current_parent = file_handler.get_parent(path)
    while current_parent != source_directory and file_handler.directory_is_empty(current_parent):
        file_handler.delete_directory(current_parent)
        current_parent = file_handler.get_parent(current_parent)


class NoMediaFileException(Exception):
    def __init__(self, message):
        super(NoMediaFileException, self).__init__(message)
