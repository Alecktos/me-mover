import sys
import logger
from file_handler import FileHandler
from file_matcher import FileMatcher
from file_mover import FileMover, CouldNotFindShowFolderException, CouldNotFindSeasonFolderException

__author__ = 'alexander.persson'


def main():
    show_name = sys.argv[1]
    destination_root = 'destination'
    file_matcher = FileMatcher()
    file_paths = file_matcher.search_files(show_name, 'sourcefolder')

    try:
        file_mover = FileMover()
        show_destination = destination_root + '/' + show_name
        file_mover.move_files(file_paths, destination_root, show_name) #TODO: borde vara move_files

    except CouldNotFindShowFolderException:
        question = 'Show folder does not exist. Create ' + show_destination + '? (yes/no)'
        user_input = raw_input(question)
        if user_input.lower().strip() is 'yes':  # TODO: refactored into module
            FileHandler.create_dir(show_destination)
            logger.log('Show folder created ' + show_destination)

    except CouldNotFindSeasonFolderException, error:
        season_path = show_destination + '/Season ' + error.season_number

        question = 'Season folder does not exist. Create ' + show_destination + '? (yes/no)'
        user_input = raw_input(question)
        if user_input.lower().strip() is 'yes':  # TODO: refactored into module
            FileHandler.create_dir(season_path)
            logger.log('Season folder created ' + season_path)
