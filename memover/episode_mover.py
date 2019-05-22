import re
import logger
import file_handler
import file_matcher
import media_file_extractor


def move(root_destination, path):
    failed_moved_files = []

    for file_path in file_handler.get_files(path):
        try:
            current_show_destination_path = __move_file_to_show_destination(
                root_destination,
                media_file_extractor.EpisodeFile(file_path)
            )

            # move all failed files to root of  show path
            for failed_moved_file_path in failed_moved_files:
                file_handler.move(
                    failed_moved_file_path,
                    current_show_destination_path + file_handler.get_last_path_part(failed_moved_file_path))
                failed_moved_files = []

        except media_file_extractor.WrongMediaTypeException:
            failed_moved_files.append(file_path)


def __move_file_to_show_destination(root_destination, episode_file):
    show_name_dir_name = __find_show_name_dir(root_destination, media_file_extractor.get_tv_show_name(episode_file.get_file_path()))
    if not show_name_dir_name:
        show_name_dir_name = __create_show_dir(root_destination, media_file_extractor.get_tv_show_name(episode_file.get_file_path()))

    season_number = str(episode_file.get_season_number())
    season_path = root_destination + '/' + show_name_dir_name + '/Season ' + season_number
    if file_handler.directory_exist(season_path):
        __remove_old_if_new_is_proper(episode_file, season_path)
    else:
        __create_season_folder(root_destination, show_name_dir_name, season_number)

    file_handler.move(episode_file.get_file_path(), season_path + '/' + episode_file.get_file_name())
    logger.log(episode_file.get_file_name() + ' moved to ' + season_path)
    return root_destination + '/' + show_name_dir_name + '/'


def __remove_old_if_new_is_proper(episodeFile, season_dir_path):
    if not episodeFile.episode_is_marked_proper():
        return

    search_query = media_file_extractor.get_tv_show_name(episodeFile.get_file_path()) + ' S' + media_file_extractor.get_season(episodeFile.get_file_path()) + ' E' + episodeFile.get_episode_number()
    files = file_matcher.search_files_with_file_type(search_query, season_dir_path, episodeFile.get_file_type())
    if len(files) is 0:
        return

    for found_file in files:
        file_handler.delete_file(found_file)


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

    # remove words with one or two letters in the beginning of the name if number of characters are bigger then five
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

    if len(found_directories) is 0 and 'proper' in search_query:
        return __find_show_name_dir(
            root_directory,
            search_query.replace('proper', '').strip()
        )  # remove proper key word, trim string and try again

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
