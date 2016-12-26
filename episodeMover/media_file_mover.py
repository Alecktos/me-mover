from media_file_extractor import MediaFileExtractor, Type
import file_handler
from episode_mover import EpisodeMover


def move_file(file_path, show_destination_path, movie_destination_path):
    """
    Moves an movie or tv-show file based on file path
    """

    media_file_extractor = MediaFileExtractor(file_path)
    media_type = media_file_extractor.get_type()
    if media_type is Type.MOVIE:
        __move_movie(media_file_extractor, movie_destination_path)

    if media_type is Type.TV_SHOW:
        __move_episode(media_file_extractor, show_destination_path)


def __move_episode(media_file_extractor, show_destination_path):
    episode_mover = EpisodeMover()

    episode_mover.move_file(show_destination_path,
                            media_file_extractor.get_tv_show_name(),
                            media_file_extractor.get_season_number(),
                            media_file_extractor.get_file_name(),
                            media_file_extractor.get_file_path())


def __move_movie(media_file_extractor, movie_destination_path):
    if not file_handler.check_directory_existance(movie_destination_path):
        raise Exception('Movie destination folder does not exist')

    file_handler.move_file(media_file_extractor.get_file_path(), media_file_extractor.get_file_name())
