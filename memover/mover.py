import episode_mover, logger
import file_matcher
from media_file_extractor import MediaFileExtractor, Type
import file_handler


def move_media_by_name(name, source_path, show_destination_path, movie_destination_path):
    paths = file_matcher.search_files(name, source_path)

    for path in paths:
        move_media_by_path(path, show_destination_path, movie_destination_path)


def move_media_by_path(file_path, show_destination_path, movie_destination_path):
    if file_handler.path_is_directory(file_path):
        for sub_file_path in file_handler.get_directory_content(file_path):
            move_media_by_path(file_path + '/' + sub_file_path, show_destination_path, movie_destination_path)
        file_handler.delete_directory(file_path)
        return

    logger.log('moving file: ' + file_path)
    media_file_extractor = MediaFileExtractor(file_path)
    media_type = media_file_extractor.get_type()
    if media_type is Type.MOVIE:
        __move_movie(media_file_extractor, movie_destination_path)
    else:
        episode_mover.move_file(show_destination_path, media_file_extractor)


def __move_movie(media_file_extractor, movie_destination_path):
    if file_handler.check_directory_existance(movie_destination_path):
        file_handler.move_file(media_file_extractor.get_file_path(), movie_destination_path + '/' + media_file_extractor.get_file_name())
    else:
        logger.log('Folder does not exist: ' + movie_destination_path)

