import episode_mover, logger
import file_matcher
from media_file_extractor import MediaFileExtractor, Type
import file_handler


def move_episodes_by_name(show_name, show_destination_root, show_source_path):
    file_paths = file_matcher.search_files(show_name, show_source_path)
    __move_episodes(show_destination_root, file_paths)


def move_media_by_path(file_path, show_destination_path, movie_destination_path):
    if file_handler.path_is_directory(file_path):
        for sub_file_path in file_handler.get_directory_content(file_path):
            move_media_by_path(file_path + '/' + sub_file_path, show_destination_path, movie_destination_path)
        file_handler.delete_directory(file_path)
        return

    media_file_extractor = MediaFileExtractor(file_path)
    media_type = media_file_extractor.get_type()
    if media_type is Type.MOVIE:
        __move_movie(media_file_extractor, movie_destination_path)
    else:
        episode_mover.move_file(show_destination_path, file_path, media_file_extractor)


def __move_movie(media_file_extractor, movie_destination_path):
    if file_handler.check_directory_existance(movie_destination_path):
        file_handler.move_file(media_file_extractor.get_file_path(), movie_destination_path + '/' + media_file_extractor.get_file_name())
    else:
        logger.log('Folder does not exist: ' + movie_destination_path)


def __move_episodes(destination_root, file_paths):
    episode_mover.move_files(file_paths, destination_root)
