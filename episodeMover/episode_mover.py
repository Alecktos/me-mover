import arguments_parser
import logger
import file_handler
from file_matcher import FileMatcher
from file_mover import FileMover, CouldNotFindShowFolderException, CouldNotFindSeasonFolderException


def main():
    show_name = arguments_parser.get_show_name()
    destination_root = arguments_parser.get_destination_path()
    file_matcher = FileMatcher()
    source_path = arguments_parser.get_source_path()
    file_paths = file_matcher.search_files(show_name, source_path)
    move_files(destination_root, file_paths, show_name)
    logger.log('Finished')


def move_files(destination_root, file_paths, show_name):
    force_create_folders = arguments_parser.in_force_mode()
    try:
        file_mover = FileMover()
        file_mover.move_files(file_paths, destination_root, show_name)

    except CouldNotFindShowFolderException:
        show_destination = destination_root + '/' + show_name
        if force_create_folders:
            logger.log('Show folder does not exist. Creating ' + show_destination)
            file_handler.create_dir(show_destination)
            logger.log(show_destination + ' created')
            move_files(destination_root, file_paths, show_name)
        else:
            logger.log(show_destination + ' folder does not exist. Runt with -f to create it')

    except CouldNotFindSeasonFolderException, error:
        season_path = destination_root + '/' + error.show_name + '/Season ' + error.season_number

        if force_create_folders:
            logger.log('Season folder does not exist. Creating ' + season_path)
            file_handler.create_dir(season_path)
            logger.log(season_path + ' created')
            move_files(destination_root, file_paths, show_name)
        else:
            logger.log(season_path + ' does not exist. Run with -f to create it')
