import episode_mover, logger, arguments_parser
from file_matcher import FileMatcher
from media_file_extractor import MediaFileExtractor, Type
import file_handler


def move_episodes_by_name(show_name, destination_root, source_path):
    file_matcher = FileMatcher()
    file_paths = file_matcher.search_files(show_name, source_path)
    __move_episodes(destination_root, file_paths)


def move_media_by_path(file_path):
    media_file_extractor = MediaFileExtractor(file_path)
    type = media_file_extractor.get_type()
    if type is Type.MOVIE:
        __move_movie(media_file_extractor)
    else:
        episode_mover.move_file(
            arguments_parser.get_shows_destination_path(),
            arguments_parser.get_source_path(),
            media_file_extractor)


def __move_movie(media_file_extractor):
    movie_path = arguments_parser.get_movies_destination_path()
    if file_handler.check_directory_existance(movie_path):
        file_handler.move_file(media_file_extractor.get_file_path(), media_file_extractor.get_file_name())
    else:
        logger.log('Folder does not exist: ' + movie_path)


def __move_episodes(destination_root, file_paths):
    episode_mover.move_files(file_paths, destination_root)
