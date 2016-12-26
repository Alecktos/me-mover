import re
import logger
import file_handler


class EpisodeMover:

    def move_files(self, sources, root_destination, show_name):
        for source in sources:
            file_name = self.__get_file_from_path(source)
            season_number = self.__get_season_number(file_name)
            self.move_file(root_destination, show_name, season_number, file_name, source)

    #todo: pass extractor object instead
    def move_file(self, root_destination, show_name, season_number, file_name, source):
        show_name_dir_name = self.__find_show_name_dir(root_destination, show_name)
        if not show_name_dir_name:
            show_name_dir_name = self.__create_show_dir(root_destination, show_name)

        season_number = str(season_number)
        season_path = root_destination + '/' + show_name_dir_name + '/Season ' + season_number
        if not file_handler.check_directory_existance(season_path):
            self.__create_season_folder(root_destination, show_name_dir_name, season_number)

        file_handler.move_file(source, season_path + '/' + file_name)
        logger.log(file_name + ' moved to ' + season_path)


    def __create_show_dir(self, root_destination, show_name):
        show_destination = root_destination + '/' + show_name
        logger.log('Show folder does not exist. Creating ' + show_destination)
        file_handler.create_dir(show_destination)
        logger.log(show_destination + ' created')
        return show_name

    def __create_season_folder(self, root_destination, show_name, season_number):
        season_path = root_destination + '/' + show_name + '/Season ' + season_number
        logger.log('Season folder does not exist. Creating ' + season_path)
        file_handler.create_dir(season_path)
        logger.log(season_path + ' created')


    def __find_show_name_dir(self, root_directory, searching_show_name):
        for directory_name in file_handler.get_subdirectories(root_directory):
            if directory_name.lower().strip() == searching_show_name.lower().strip():
                return directory_name
        return None

    def __get_season_number(self, file_name):
        pattern = re.compile('[.][Ss](\d+)[Ee]\d+[.]')
        match_object = pattern.search(file_name)
        if match_object is None:
            raise Exception('Can not determine season in name')

        season_number = match_object.group(1)  # gives the math in name
        return season_number.lstrip('0')

    def __is_right_season_directory(self, path, season_number):
        season_name = 'Season ' + str(season_number)
        print path
        if season_name in path:
            return True
        return False

    def __get_file_from_path(self, path):
        file_name_index = path.rfind('/')
        return path[file_name_index + 1:]

