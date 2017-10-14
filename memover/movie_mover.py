import file_handler
import logger


def move(movie_destination_path, media_file_extractor):
    if file_handler.check_directory_existance(movie_destination_path):
        file_handler.move_file(media_file_extractor.get_file_path(), movie_destination_path + '/' + media_file_extractor.get_file_name())
    else:
        logger.log('Folder does not exist: ' + movie_destination_path)