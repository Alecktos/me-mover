# coding=utf-8
import os
import re
import file_handler
import show_name_extractor


__MEDIA_FILE_MIN_FILE_SIZE_MB = 50


class Type:
    MOVIE = 0
    TV_SHOW = 1


def is_media_file(file_path):
    return file_handler.get_file_size(file_path) >= __MEDIA_FILE_MIN_FILE_SIZE_MB


def get_type(path):
    if __path_contains_multiple_tv_episodes(path):
        return Type.TV_SHOW

    if __path_contains_at_least_one_episode(path):
        return Type.TV_SHOW

    return Type.MOVIE


def __path_contains_multiple_tv_episodes(path):
    episode_numbers = sorted(list(iterate_episodes_numbers(path)))

    min_number_of_episodes = 5
    if len(episode_numbers) < min_number_of_episodes:
        return False

    for index, element in enumerate(episode_numbers[1:], start=1):
        if element is not episode_numbers[index-1] + 1:
            return False

    return True


def iterate_episodes_numbers(path):
    for file_path in file_handler.get_files(path):
        if is_media_file(file_path) and __contains_episode_number(file_path):
            yield int(_get_episode_number_matches(file_path)[0][0])


def __contains_episode_number(file_path):
    matches = _get_episode_number_matches(file_path)
    return len(matches) is 1


def _get_episode_number_matches(file_path):
    return re.findall(r'((?<=(\s|_))\d+(?=(\s|_)))', file_path)


def _get_show_name(file_path):
    show_name = re.search(r'.*(?=(\s|_)\d+(\s|_))', file_path)
    if show_name:
        return show_name.group(0)
    return None


def __path_contains_at_least_one_episode(path):
    for file_path in file_handler.get_files(path):
        reg_tv_result = _get_episode_info(file_path)  # if we found episode info media_type is TV SHOW.
        if reg_tv_result is not None:
            return True
    return False


def _get_episode_info(path):
    match = __match_episode(path)

    # check if parent folder gives a episode match when a fallback to movie has been made
    if match is None:
        parent_path = path.split('/')[-2]
        match = __match_episode(parent_path)

    return match


def __match_episode(path):
    """
    :param path: a path to something that is assumed to be a episode
    :return: extracted episode data (season, episode, show name)
    """
    file_basename = file_handler.get_last_path_part(path)
    reg_tv = re.compile('(.+?)[ .][Ss](\d\d?)[Ee](\d\d?).*?(?:[ .](\d{3}\d?p)|\Z)?')
    match = reg_tv.match(file_basename)

    if match is None:
        reg_tv = re.compile(r'(.+)[\s?][-?][\s](\d\d?)[Xx](\d\d?)[\s](.+)')
        match = reg_tv.match(file_basename)

    return match


class MovieFile:
    def __init__(self, file_path):
        self.__file_path = file_path

    def get_file_path(self):
        return self.__file_path

    def get_file_name(self):
        return file_handler.get_last_path_part(self.__file_path)

    def get_movie_name(self, source_root_path):
        return file_handler.get_last_name_from_path(source_root_path)


class EpisodeFile:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__file_name = os.path.basename(file_path)
        reg_tv_result = _get_episode_info(self.__file_path)

        if reg_tv_result is not None:
            show_name = reg_tv_result.group(1)
            season = reg_tv_result.group(2)
            episode = reg_tv_result.group(3)
        else:
            # fallback on just getting the episode number and assuming it's first season
            local_file = file_handler.get_last_path_part(file_path)
            matches = _get_episode_number_matches(local_file)
            show_name = _get_show_name(local_file)

            if len(matches) is 0 or not show_name:
                raise WrongMediaTypeException('Can not parse episode')

            episode = matches[0]
            season = '01'

        self.__match = {
            'show_name': show_name,
            'season': season,
            'episode': episode
        }

    def get_file_path(self):
        return self.__file_path

    def get_file_name(self):
        return self.__file_name

    def get_tv_show_name(self):
        return show_name_extractor.extract_delete_test_dirs_show_name(self.__match['show_name'])

    def get_season(self):
        """
        :return: the original season number from file name
        """
        return self.__match['season']

    def get_season_number(self):
        """
        :return: the season number in form of an integer value
        """
        return int(self.__match['season'])

    def get_episode_number(self):
        return self.__match['episode']

    def episode_is_marked_proper(self):
        return '.proper.' in self.__file_name.lower()

    def get_file_type(self):
        return file_handler.get_file_type(self.get_file_path())


class WrongMediaTypeException(Exception):
    def __init__(self, message):
        super(WrongMediaTypeException, self).__init__(message)
