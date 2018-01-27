# coding=utf-8
import os
import re
import file_handler
import show_name_extractor


class Type:
    MOVIE = 0
    TV_SHOW = 1


def get_type(path):
    for file_path in file_handler.get_files(path):
        reg_tv_result = _get_episode_info(file_path)  # if we found episode info media_type is TV SHOW.
        if reg_tv_result is not None:
            return Type.TV_SHOW

    return Type.MOVIE


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
    return reg_tv.match(file_basename)


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
        self.__reg_tv_result = _get_episode_info(self.__file_path)

        if self.__reg_tv_result is None:
            raise WrongMediaTypeException('Can not parse episode')

    def get_file_path(self):
        return self.__file_path

    def get_file_name(self):
        return self.__file_name

    def get_tv_show_name(self):
        return show_name_extractor.extract_delete_test_dirs_show_name(self.__reg_tv_result.group(1))

    def get_season(self):
        """
        :return: the original season number from file name
        """
        return self.__reg_tv_result.group(2)

    def get_season_number(self):
        """
        :return: the season number in form of an integer value
        """
        return int(self.__reg_tv_result.group(2))

    def get_episode_number(self):
        return self.__reg_tv_result.group(3)

    def episode_is_marked_proper(self):
        return '.proper.' in self.__file_name.lower()

    def get_file_type(self):
        return file_handler.get_file_type(self.get_file_path())


class WrongMediaTypeException(Exception):
    def __init__(self, message):
        super(WrongMediaTypeException, self).__init__(message)
