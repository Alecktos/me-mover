import arguments_parser
from arguments_parser import Arguments
import logger
import mover


def main():
    command = arguments_parser.get_command()
    if command is None:
        logger.log('No Command')
        return

    if command == arguments_parser.Commands.SHOW:
        logger.log('moving on show name')
        __move_based_on_show()
        return

    if command == arguments_parser.Commands.FILE:
        logger.log('moving on file path')
        __move_based_on_file()
        return

    logger.log('No action was made')


def __move_based_on_show():
    show_name = arguments_parser.get_show_name(),
    show_destination_path = arguments_parser.get_shows_destination_path(),
    show_source_path = arguments_parser.get_show_source_path()

    arguments = {
        Arguments.SHOW_NAME: show_name,
        Arguments.SHOW_DESTINATION: show_destination_path,
        Arguments.SHOW_SOURCE: show_source_path
    }

    if not __arguments_are_valid(arguments):
        return

    mover.move_episodes_by_name(
        arguments_parser.get_show_name(),
        arguments_parser.get_shows_destination_path(),
        arguments_parser.get_show_source_path())


def __move_based_on_file():
    file_path = arguments_parser.get_file_path()
    show_destination_path = arguments_parser.get_shows_destination_path()
    show_source_path = arguments_parser.get_show_source_path()
    movie_destination_path = arguments_parser.get_movies_destination_path()

    arguments = {
        Arguments.FILE_PATH: file_path,
        Arguments.SHOW_DESTINATION: show_destination_path,
        Arguments.SHOW_SOURCE: show_source_path,
        Arguments.MOVIE_DESTINATION: movie_destination_path
    }

    if not __arguments_are_valid(arguments):
        return

    mover.move_media_by_path(file_path, show_destination_path, movie_destination_path, show_source_path)


def __arguments_are_valid(arguments):
    for key, value in arguments.iteritems():
        if value is None:
            logger.log('missing argument: ' + key)
            return False
    return True

