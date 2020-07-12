import re

from . import file_handler
from . import file_matcher
from . import logger
from . import media_file_extractor


def move(root_destination, path):
    failed_moved_files = []
    current_show_destination_path = None

    for file_path in file_handler.get_files(path):
        try:
            current_show_destination_path = __move_file_to_show_destination(
                root_destination,
                file_path
            )

        except media_file_extractor.WrongMediaTypeException:
            failed_moved_files.append(file_path)

    # move all failed files to root of show path
    if current_show_destination_path:
        for failed_moved_file_path in failed_moved_files:
            file_handler.move(
                failed_moved_file_path,
                current_show_destination_path + file_handler.get_last_path_part(failed_moved_file_path))


def __move_file_to_show_destination(root_destination, file_path):
    show_name_dir_name = __find_show_name_dir(root_destination, media_file_extractor.get_tv_show_name(file_path))
    if not show_name_dir_name:
        show_name_dir_name = __create_show_dir(root_destination, media_file_extractor.get_tv_show_name(file_path))

    season_number = str(media_file_extractor.get_season_number(file_path))
    season_path = root_destination + '/' + show_name_dir_name + '/Season ' + season_number
    if file_handler.directory_exist(season_path):
        __remove_old_if_new_is_proper(file_path, season_path)
    else:
        __create_season_folder(root_destination, show_name_dir_name, season_number)

    file_handler.move(file_path, season_path + '/' + file_handler.get_last_path_part(file_path))
    logger.info('"' + file_path + '" moved to: "' + season_path + '"')
    return root_destination + '/' + show_name_dir_name + '/'


def __remove_old_if_new_is_proper(file_path, season_dir_path):
    if not media_file_extractor.episode_is_marked_proper(file_path):
        return

    search_query = media_file_extractor.get_tv_show_name(file_path) + ' S' + media_file_extractor.get_season(file_path) + ' E' + media_file_extractor.get_episode_number(file_path)
    files = file_matcher.search_files_with_file_type(search_query, season_dir_path, media_file_extractor.get_file_type(file_path))
    if len(files) == 0:
        return

    for found_file in files:
        file_handler.delete_file(found_file)


def __create_show_dir(root_destination, show_name):
    show_destination = root_destination + '/' + show_name
    logger.debug('Directory does not exist. Creating: ' + show_destination)
    file_handler.create_dir(show_destination)
    return show_name


def __create_season_folder(root_destination, show_name, season_number):
    season_path = root_destination + '/' + show_name + '/Season ' + season_number
    logger.debug('Directory does not exist. Creating: ' + season_path)
    file_handler.create_dir(season_path)


def __find_show_name_dir(root_directory, searching_show_name):
    search_query = searching_show_name.lower().strip()

    logger.debug('Searching for matching directories with query: "' + search_query + '".')

    found_directories = __find_matching_directories(root_directory, search_query)
    if len(found_directories) == 1:
        return found_directories[0]

    # remove words with one or two letters in the beginning of the name if number of characters are bigger then five
    if len(search_query) > 5 and len(search_query.split()) >= 2:
        shortword_regex = re.compile(r'^\w{1,2}\b|\b\w{1,2}$')
        search_query = shortword_regex.sub('', search_query)

    found_directories = __find_matching_directories(root_directory, search_query)

    if len(found_directories) > 1:
        raise MultipleDirectoryMatchesException(searching_show_name, root_directory, found_directories)

    if len(found_directories) == 0 and 'proper' in search_query:
        return __find_show_name_dir(
            root_directory,
            search_query.replace('proper', '').strip()
        )  # remove proper key word, trim string and try again

    if len(found_directories) == 0:
        return None

    return found_directories[0]


def __is_right_season_directory(path, season_number):
    season_name = 'Season ' + str(season_number)
    if season_name in path:
        return True
    return False


def __find_matching_directories(root_directory, search_query):
    return [dir_name for dir_name in file_handler.get_directory_content(root_directory) if
                         search_query in dir_name.lower().strip()]


class MultipleDirectoryMatchesException(Exception):

    def __init__(self, show_name, destination_folder, matching_dirs):
        matches = ', '.join(matching_dirs)
        super(MultipleDirectoryMatchesException, self).__init__(
            f'{show_name} matches multiple directories when moved {destination_folder}. Matches: {matches}'
        )
