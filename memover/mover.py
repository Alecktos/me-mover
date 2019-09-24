from . import episode_mover
from . import logger
from . import file_matcher
from .media_file_extractor import get_type, Type
from . import file_handler
from . import movie_mover
from . import subtitles


def move_media_by_name(name, source_path, show_destination_path, movie_destination_path):
    paths = file_matcher.search_files(name, source_path)

    for path in paths:
        move_media_by_path(path, show_destination_path, movie_destination_path)


def move_media_by_path(path, show_destination_path, movie_destination_path):
    subtitles.rename_and_move(path)
    logger.log('moving file/dir: ' + path)
    media_type = get_type(path)
    if media_type is Type.MOVIE:
        movie_mover.move(movie_destination_path, path)
    else:
        episode_mover.move(show_destination_path, path)

    if file_handler.path_is_directory(path):
        file_handler.delete_directory(path)