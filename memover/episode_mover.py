import logger
import file_handler
from media_file_extractor import MediaFileExtractor


def move_files(sources, root_destination):
    for source in sources:
        media_file_extractor = MediaFileExtractor(source)
        move_file(root_destination, source, media_file_extractor)


def move_file(root_destination, source, media_file_extractor):
    show_name_dir_name = __find_show_name_dir(root_destination, media_file_extractor.get_tv_show_name())
    if not show_name_dir_name:
        show_name_dir_name = __create_show_dir(root_destination, media_file_extractor.get_tv_show_name())

    season_number = str(media_file_extractor.get_season_number())
    season_path = root_destination + '/' + show_name_dir_name + '/Season ' + season_number
    if not file_handler.check_directory_existance(season_path):
        __create_season_folder(root_destination, show_name_dir_name, season_number)

    file_handler.move_file(source, season_path + '/' + media_file_extractor.get_file_name())
    logger.log(media_file_extractor.get_file_name() + ' moved to ' + season_path)


def __create_show_dir(root_destination, show_name):
    show_destination = root_destination + '/' + show_name
    logger.log('Show folder does not exist. Creating ' + show_destination)
    file_handler.create_dir(show_destination)
    logger.log(show_destination + ' created')
    return show_name


def __create_season_folder(root_destination, show_name, season_number):
    season_path = root_destination + '/' + show_name + '/Season ' + season_number
    logger.log('Season folder does not exist. Creating ' + season_path)
    file_handler.create_dir(season_path)
    logger.log(season_path + ' created')


def __find_show_name_dir(root_directory, searching_show_name):
    for directory_name in file_handler.get_subdirectories(root_directory):
        if directory_name.lower().strip() == searching_show_name.lower().strip():
            return directory_name
    return None


def __is_right_season_directory(path, season_number):
    season_name = 'Season ' + str(season_number)
    print path
    if season_name in path:
        return True
    return False
