import sys
import logger
from file_handler import FileHandler
from file_matcher import FileMatcher
from file_mover import FileMover, CouldNotFindShowFolderException, CouldNotFindSeasonFolderException

__author__ = 'alexander.persson'


def main():
    show_name = sys.argv[1]

    if 2 in sys.argv:
        if sys.argv[2] == '-f':
            force_create_folders = True
        else:
            force_create_folders = False

    destination_root = 'destination'
    file_matcher = FileMatcher()
    file_paths = file_matcher.search_files(show_name, 'sourcefolder')
    show_destination = destination_root + '/' + show_name

    try:
        file_mover = FileMover()
        file_mover.move_files(file_paths, destination_root, show_name) #TODO: borde vara move_files

    except CouldNotFindShowFolderException:
        if force_create_folders:
            print 'Show folder does not exist. Creating ' + show_destination
            FileHandler.create_dir(show_destination)
            logger.log(show_destination + ' created')
        else:
            print 'Show folder does not exist. Runt with -f to create it'

    except CouldNotFindSeasonFolderException, error:
        season_path = show_destination + '/Season ' + error.season_number

        if force_create_folders:
            print 'Season folder does not exist. Creating ' + season_path
            FileHandler.create_dir(season_path)
            logger.log(season_path + ' created')
        else:
            print season_path + ' does not exist. Run with -f to create it'
