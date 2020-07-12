# coding=utf-8
import re

from . import file_handler
from . import show_name_extractor

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


def get_season(file_path):
    """
    :return: the original season number from file name
    """
    match = _get_episode_match(file_path)
    return match['season']


def get_season_number(file_path):
    """
    :return: the season number in form of an integer value
    """
    match = _get_episode_match(file_path)
    return int(match['season'])


def get_episode_number(file_path):
    """
        use with care. All episodes doe not have episode number
        :return: the episode number or None
    """
    match = _get_episode_match(file_path)
    return match['episode']


def get_tv_show_name(file_path):
    match = _get_episode_match(file_path)
    return show_name_extractor.extract_delete_test_dirs_show_name(match['show_name'])


def get_file_type(file_path):
    return file_handler.get_file_type(file_path)


def episode_is_marked_proper(file_path):
    file_name = file_handler.get_last_path_part(file_path)
    return '.proper.' in file_name.lower()


def __path_contains_multiple_tv_episodes(path):
    episode_numbers = sorted(list(_iterate_episodes_numbers(path)))

    min_number_of_episodes = 5
    if len(episode_numbers) < min_number_of_episodes:
        return False

    for index, element in enumerate(episode_numbers[1:], start=1):
        # Allow same or one less
        if element is not episode_numbers[index-1] + 1 and element is not episode_numbers[index-1]:
            return False

    return True


def _iterate_episodes_numbers(path):
    for file_path in file_handler.get_files(path):
        if is_media_file(file_path) and __contains_episode_number(file_path):
            yield int(_get_episode_number_matches(file_path)[0])


def __contains_episode_number(file_path):
    matches = _get_episode_number_matches(file_path)
    return len(matches) > 0


def _get_episode_number_matches(file_path):
    file = '/' + file_handler.get_last_path_part(file_path) # Add slash for regex compability
    matches = re.findall(r'(?<=\s|_|E|\/)\d+(?=\s|\w|\[)', file)
    return matches


def _get_show_name(file_path):
    local_path = file_handler.get_last_path_part(file_path)
    show_name = re.search(r'.*(?=(\s|_)\d+(\s|_))', local_path)
    if show_name:
        if show_name.group(0).lower() != 'episode':
            return show_name.group(0)
    parent_path = file_handler.get_parent(file_path)  # fall back on parent hoping it contains show name
    return file_handler.get_last_path_part(parent_path)


def __path_contains_at_least_one_episode(path):
    for file_path in file_handler.get_files(path):
        reg_tv_result = _get_episode_info(file_path)  # if we found episode info media_type is TV SHOW.
        if reg_tv_result is not None:
            return True
    return False


def _get_episode_info(path):
    match = __match_episode(path)

    # check if parent folder gives a episode match
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
    reg_tv = re.compile('(.+?)[. ][Ss](\d\d?)[ .Ee]((\d\d?)?).*')
    match = reg_tv.match(file_basename)

    if match is None:
        reg_tv = re.compile(r'(.+)[\s?][-?][\s](\d\d?)[Xx](\d\d?)[\s](.+)')
        match = reg_tv.match(file_basename)

    return match


def _get_episode_match(file_path):
    reg_tv_result = _get_episode_info(file_path)

    if reg_tv_result is not None:
        show_name = reg_tv_result.group(1)
        season = reg_tv_result.group(2)
        episode = reg_tv_result.group(4)
    else:
        # fallback on just getting the episode number and assuming it's first season
        matches = _get_episode_number_matches(file_path)
        show_name = _get_show_name(file_path)

        if len(matches) == 0 or not show_name:
            raise WrongMediaTypeException('Can not parse episode')

        episode = matches[0]
        season = '01'

    return {
        'show_name': show_name,
        'season': season,
        'episode': episode
    }


class WrongMediaTypeException(Exception):
    def __init__(self, message):
        super(WrongMediaTypeException, self).__init__(message)
