import sys
import logger
import file_handler
from file_matcher import FileMatcher
from file_mover import FileMover, CouldNotFindShowFolderException, CouldNotFindSeasonFolderException

__author__ = 'alexander.persson'


def main():
    show_name = sys.argv[1]

    force_create_folders = False
    if len(sys.argv) >= 3 and sys.argv[2] == '-f':
        force_create_folders = True

    destination_root = 'destination'  # /media/MEDIA/SERIER
    file_matcher = FileMatcher()
    file_paths = file_matcher.search_files(show_name, 'sourcefolder')  # /media/MEDIA/FINISHED
    if len(file_paths) is 0:
        logger.log('No matching files found')

    move_files(destination_root, file_paths, force_create_folders, show_name)
    logger.log('Finished')


def move_files(destination_root, file_paths, force_create_folders, show_name):
    try:
        file_mover = FileMover()
        file_mover.move_files(file_paths, destination_root, show_name)

    except CouldNotFindShowFolderException:
        show_destination = destination_root + '/' + show_name
        if force_create_folders:
            logger.info('Show folder does not exist. Creating ' + show_destination)
            file_handler.create_dir(show_destination)
            logger.log(show_destination + ' created')
            move_files(destination_root, file_paths, force_create_folders, show_name)
        else:
            logger.log(show_destination + ' folder does not exist. Runt with -f to create it')

    except CouldNotFindSeasonFolderException, error:
        season_path = destination_root + '/' + error.show_name + '/Season ' + error.season_number

        if force_create_folders:
            logger.log('Season folder does not exist. Creating ' + season_path)
            file_handler.create_dir(season_path)
            logger.log(season_path + ' created')
            move_files(destination_root, file_paths, force_create_folders, show_name)
        else:
            logger.log(season_path + ' does not exist. Run with -f to create it')
