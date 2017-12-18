import arguments_parser
from arguments_parser import Arguments
import logger
import mover
import subtitles


def main():
    command = arguments_parser.get_command()
    if command is None:
        logger.log('No Command')
        return

    if command == arguments_parser.Commands.NAME:
        def move_function():
            mover.move_media_by_name(
                arguments_parser.get_show_name(),
                arguments_parser.get_source_path(),
                arguments_parser.get_shows_destination_path(),
                arguments_parser.get_movies_destination_path()
            )
        __move_media(move_function)
        return

    if command == arguments_parser.Commands.FILE:
        def move_function():
            mover.move_media_by_path(
                arguments_parser.get_file_path(),
                arguments_parser.get_shows_destination_path(),
                arguments_parser.get_movies_destination_path()
            )

        __move_media(move_function)
        return

    logger.log('No action was made')


def __move_media(move_function):
    subtitles.rename_and_move(arguments_parser.get_source_path())
    move_function()
