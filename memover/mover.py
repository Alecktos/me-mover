import episode_mover
import logger
import file_matcher
from media_file_extractor import get_type, Type, MovieFile, EpisodeFile
import file_handler
import movie_mover


def move_media_by_name(name, source_path, show_destination_path, movie_destination_path):
    paths = file_matcher.search_files(name, source_path)

    for path in paths:
        move_media_by_path(path, show_destination_path, movie_destination_path)


def move_media_by_path(file_path, show_destination_path, movie_destination_path):
    if file_handler.path_is_directory(file_path):
        for sub_file_path in file_handler.get_directory_content(file_path):
            __move_media_file(file_path + '/' + sub_file_path, show_destination_path, movie_destination_path, file_path)
        file_handler.delete_directory(file_path)
        return

    __move_media_file(file_path, show_destination_path, movie_destination_path, file_path)


def __move_media_file(file_path, show_destination_path, movie_destination_path, source_root_path):
    logger.log('moving file: ' + file_path)
    media_type = get_type(file_path)
    if media_type is Type.MOVIE:
        movie_mover.move(movie_destination_path, MovieFile(file_path), source_root_path)
    else:
        episode_mover.move_file(show_destination_path, EpisodeFile(file_path))
