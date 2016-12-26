import arguments_parser
import logger
import file_handler
from file_matcher import FileMatcher
from episode_mover import EpisodeMover
from media_file_extractor import MediaFileExtractor, Type


def main():
    destination_root = arguments_parser.get_shows_destination_path()
    file_matcher = FileMatcher()
    source_path = arguments_parser.get_source_path()

    show_name = arguments_parser.get_show_name()
    if show_name:
        file_paths = file_matcher.search_files(show_name, source_path)
        __move_episode_based_on_name(destination_root, file_paths, show_name)
        logger.log('Finished')
        return

    file_path = arguments_parser.get_file_path()
    if file_path:
        __move_media_based_on_path(file_path)
        logger.log('Finished')

    logger.log('No action was made')



def __move_media_based_on_path(file_path):
    media_file_extractor = MediaFileExtractor(file_path)
    type = media_file_extractor.get_type()
    if type is Type.MOVIE:
        movie_path = arguments_parser.get_movies_destination_path()
        if file_handler.check_directory_existance(movie_path):
            file_handler.move_file(file_path, media_file_extractor.get_file_name())
        else:
            logger.log('Folder does not exist: ' + movie_path)


def __move_episode_based_on_name(destination_root, file_paths, show_name):
    # only support moves episodes, not movies based on name
    episode_mover = EpisodeMover()
    episode_mover.move_files(file_paths, destination_root, show_name)