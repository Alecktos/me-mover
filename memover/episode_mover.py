import re

import logger
import file_handler


def move_file(root_destination, media_file_extractor):
    show_name_dir_name = __find_show_name_dir(root_destination, media_file_extractor.get_tv_show_name())
    if not show_name_dir_name:
        show_name_dir_name = __create_show_dir(root_destination, media_file_extractor.get_tv_show_name())

    season_number = str(media_file_extractor.get_season_number())
    season_path = root_destination + '/' + show_name_dir_name + '/Season ' + season_number
    if not file_handler.check_directory_existance(season_path):
        __create_season_folder(root_destination, show_name_dir_name, season_number)

    file_handler.move_file(media_file_extractor.get_file_path(), season_path + '/' + media_file_extractor.get_file_name())
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
    search_query = searching_show_name

    # remove words with one or two letters int the beginning of the name if number of characters are bugger then five
    if len(search_query) > 5 and len(search_query.split()) >= 2:
        shortword_regex = re.compile(r'^\w{1,2}\b|\b\w{1,2}$')
        search_query = shortword_regex.sub('', search_query)

    search_query = search_query.lower().strip()

    logger.log('searching for matching folders in ' + root_directory + ' for query "' + search_query + '". Searching show name: "' + searching_show_name + '"')

    found_directories = filter(
        lambda dir_name: search_query in dir_name.lower().strip(),
        file_handler.get_directory_content(root_directory)
    )

    if len(found_directories) > 1:
        raise MultipleDirectoryMatchesException(searching_show_name, root_directory)

    if len(found_directories) is 0:
        return None

    return found_directories[0]


def __is_right_season_directory(path, season_number):
    season_name = 'Season ' + str(season_number)
    print path
    if season_name in path:
        return True
    return False


class MultipleDirectoryMatchesException(Exception):

    def __init__(self, show_name, destination_folder):
        super(MultipleDirectoryMatchesException, self).__init__(
            show_name + ' matches multiple directories in ' + destination_folder
        )
