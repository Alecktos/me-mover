# coding=utf-8
import os
import re


class Type:
    MOVIE = 0
    TV_SHOW = 1


class MediaFileExtractor:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__file_name = os.path.basename(file_path)
        reg_tv = re.compile('(.+?)[ .]S(\d\d?)E(\d\d?).*?(?:[ .](\d{3}\d?p)|\Z)?')
        self.__reg_tv_result = reg_tv.match(self.__file_name)
        self.__type = self.__extract_type()

    def get_file_path(self):
        return self.__file_path

    def get_file_name(self):
        return self.__file_name

    def __extract_type(self):
        if self.__reg_tv_result is None:
            return Type.MOVIE
        return Type.TV_SHOW

    def get_type(self):
        return self.__type

    def get_tv_show_name(self):
        if self.get_type() is Type.MOVIE:
            raise WrongMediatypeException('Wrong media type')

        return self.__reg_tv_result.group(1).replace('.', ' ')

    def get_season_number(self):
        if self.get_type() is Type.MOVIE:
            raise WrongMediatypeException('Wrong media type')

        return int(self.__reg_tv_result.group(2))

    def get_episode_number(self):
        if self.get_type() is Type.MOVIE:
            raise WrongMediatypeException('Wrong media type')

        return self.__reg_tv_result.group(3)


class WrongMediatypeException(Exception):
    def __init__(self, message):
        super(WrongMediatypeException, self).__init__(message)