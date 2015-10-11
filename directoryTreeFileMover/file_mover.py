import os
import re
import logger
from file_handler import FileHandler


class FileMover:

    def move_files(self, sources, root_destination, show_name):
        for source in sources:
            self.__move_file(source, root_destination, show_name)

    def __move_file(self, source, root_destination, show_name):
        file_name = self.__get_file_from_path(source)
        season_number = self.__get_season_number(file_name)
        show_name = self.__find_show_name(root_destination, show_name)
        if not show_name:
            raise CouldNotFindShowFolderException('Could not find matching show name')

        season_path = root_destination + '/' + show_name + '/Season ' + str(season_number)
        if os.path.isdir(season_path):
            file_handler = FileHandler()
            file_handler.move_file(source, season_path + '/' + file_name)
            logger.log(file_name + ' moved to ' + season_path)
        else:
            raise CouldNotFindSeasonFolderException('could not found matching season folder', season_number)

    def __find_show_name(self, root_directory, searching_show_name):
        for root, directories, files in os.walk(root_directory, topdown=True):
            for directory in directories:
                if directory.lower().strip() == searching_show_name.lower().strip():
                    return directory
        return None

    def __get_season_number(self, file_name):
        pattern = re.compile('[.][Ss](\d+)[Ee]\d+[.]')
        match_object = pattern.search(file_name)
        if match_object is None:
            raise Exception('Can not determine season in name')

        season_number = match_object.group(1)  # gives the math in name
        return season_number.lstrip('0')

    def __is_directory(self, path):
        return os.path.isdir(path)

    def __is_right_season_directory(self, path, season_number):
        season_name = 'Season ' + str(season_number)
        print path
        if season_name in path:
            return True
        return False

    def __get_file_from_path(self, path):
        file_name_index = path.rfind('/')
        return path[file_name_index + 1:]


class CouldNotFindShowFolderException(Exception):

        def __init__(self, message):
            super(CouldNotFindShowFolderException, self).__init__(message)


class CouldNotFindSeasonFolderException(Exception):

        def __init__(self, message, season_number):
            super(CouldNotFindSeasonFolderException, self).__init__(message)
            self.season_number = season_number
