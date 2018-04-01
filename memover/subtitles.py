from memover import file_handler, media_file_extractor

__subtitle_types = ('.srt', '.smi', '.ssa', '.ass', '.vtt')
__subtitle_language_annotations = {'eng': '.en'}


def rename_and_move(source_directory):
    if not file_handler.path_is_directory(source_directory):
        return

    for file_path in file_handler.get_files(source_directory):

        if file_path.endswith(__subtitle_types) and __subtitle_should_be_moved(file_path):
            __move_subtitle(file_path, source_directory)


def __subtitle_should_be_moved(subtitle_path):
    biggest_file = file_handler.get_biggest_file(file_handler.get_parent(subtitle_path))
    if not media_file_extractor.is_media_file(biggest_file.path):
        return True

    # check if subtitle file name includes any of supported language annotations
    if not any(substring in subtitle_path for substring in __subtitle_language_annotations.itervalues()):
        return True

    biggest_file_name = file_handler.get_last_path_part(biggest_file.path)
    biggest_file_without_extension = file_handler.get_path_without_extension(biggest_file_name)

    subtitle_file_name = file_handler.get_last_path_part(subtitle_path)

    # should be moved if subtitle is not already named after media file in directory
    return subtitle_file_name.find(biggest_file_without_extension) is -1


def __move_subtitle(subtitle_path, source_directory):
    for biggest_file in file_handler.get_biggest_files(file_handler.get_parent(subtitle_path), source_directory):
        if media_file_extractor.is_media_file(biggest_file.path):

            index = __number_of_subtitles_in_directory(
                file_handler.get_parent(biggest_file.path),
                subtitle_path
            )

            __rename_file(
                subtitle_path,
                file_handler.get_path_without_extension(biggest_file.path),
                index
            )
            __delete_empty_parents(subtitle_path, source_directory)
            break


def __number_of_subtitles_in_directory(dir_path, source_subtitle_path):
    subtitles = filter(
        lambda path: path.endswith(__subtitle_types) and file_handler.get_last_path_part(source_subtitle_path) != path,
        file_handler.get_directory_content(dir_path)
    )
    return len(subtitles)


def __rename_file(subtitle_source_path, media_file_path_without_extension, index):
    subtitle_type = file_handler.get_file_type(subtitle_source_path)
    index_name = '' if index == 0 else str(index + 1)

    destination_path = media_file_path_without_extension + __subtitle_language_annotations.get('eng') + index_name + subtitle_type

    # assuming all subs are english for now
    file_handler.move_file(
        subtitle_source_path,
        destination_path
    )


def __delete_empty_parents(path, source_directory):

    current_parent = file_handler.get_parent(path)
    while current_parent != source_directory and file_handler.directory_is_empty(current_parent):
        file_handler.delete_directory(current_parent)
        current_parent = file_handler.get_parent(current_parent)


class NoMediaFileException(Exception):
    def __init__(self, message):
        super(NoMediaFileException, self).__init__(message)