import arguments_parser
import logger
import mover


def main():
    command = arguments_parser.get_command()
    if command is None:
        logger.log('No Command')
        return

    if command == arguments_parser.Commands.NAME:
        mover.move_media_by_name(
            arguments_parser.get_show_name(),
            arguments_parser.get_source_path(),
            arguments_parser.get_shows_destination_path(),
            arguments_parser.get_movies_destination_path()
        )
        return

    if command == arguments_parser.Commands.FILE:
        mover.move_media_by_path(
            arguments_parser.get_file_path(),
            arguments_parser.get_shows_destination_path(),
            arguments_parser.get_movies_destination_path()
        )
        return

    logger.log('No action was made')
