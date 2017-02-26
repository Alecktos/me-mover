# coding=utf-8
import os
import re
import datetime


class Type:
    MOVIE = 0
    TV_SHOW = 1


class MediaFileExtractor:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__file_name = os.path.basename(file_path)
        self.__reg_tv_result = self.__match_path(self.__file_name)
        self.__type = self.__extract_type()
        if self.__type is Type.MOVIE:
            parent_name = file_path.split('/')[-2]
            self.__reg_tv_result = self.__match_path(parent_name)
            self.__type = self.__extract_type()

    def get_file_path(self):
        return self.__file_path

    def get_file_name(self):
        return self.__file_name

    def get_type(self):
        return self.__type

    def get_tv_show_name(self):
        if self.get_type() is Type.MOVIE:
            raise WrongMediaTypeException('Wrong media type')

        show_name_words = self.__reg_tv_result.group(1)\
            .replace('.', ' ')\
            .split()

        return self.__extract_release_date(show_name_words)

    def get_season(self):
        """
        :return: the original season number from file name
        """

        if self.get_type() is Type.MOVIE:
            raise WrongMediaTypeException('Wrong media type')

        return self.__reg_tv_result.group(2)

    def get_season_number(self):
        """
        :return: the season number in form of an integer value
        """

        if self.get_type() is Type.MOVIE:
            raise WrongMediaTypeException('Wrong media type')

        return int(self.__reg_tv_result.group(2))

    def get_episode_number(self):
        if self.get_type() is Type.MOVIE:
            raise WrongMediaTypeException('Wrong media type')

        return self.__reg_tv_result.group(3)

    def episode_is_marked_proper(self):
        return '.proper.' in self.__file_name.lower()

    def __extract_type(self):
        if self.__reg_tv_result is None:
            return Type.MOVIE
        return Type.TV_SHOW

    @staticmethod
    def __match_path(file_name):
        reg_tv = re.compile('(.+?)[ .][Ss](\d\d?)[Ee](\d\d?).*?(?:[ .](\d{3}\d?p)|\Z)?')
        return reg_tv.match(file_name)

    @staticmethod
    def __extract_release_date(show_name_words):
        d1 = datetime.date(2000, 1, 1)
        d2 = datetime.date.today()

        try:
            last_word_date = datetime.datetime.strptime(show_name_words[-1], '%Y').date()
            if d1 <= last_word_date <= d2:
                del show_name_words[-1]
        finally:
            return ' '.join(show_name_words)


class WrongMediaTypeException(Exception):
    def __init__(self, message):
        super(WrongMediaTypeException, self).__init__(message)
