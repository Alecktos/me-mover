import os
import re
from file_handler import FileHandler


class FileMover:

    def move_file(self, source, root_destination, show_name):
        file_name = self.__get_file_from_path(source)
        season_number = self.__get_season_number(file_name)
        season_path = (root_destination + '/' + show_name + '/Season '
                       + str(season_number))

        if os.path.isdir(season_path):
            file_handler = FileHandler()
            file_handler.move_file(source, season_path + '/' + file_name)

    def __get_season_number(self, file_name):
        pattern = re.compile('[.][S](\d+)[E]\d+[.]')
        match_object = pattern.search(file_name)
        if match_object is None:
            raise Exception('Can not determine season in name')

        season_number = match_object.group(1)  # gives me the math in name
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
