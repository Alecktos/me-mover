import arguments_parser
import logger
import mover


def main():
    episodes_destination_root = arguments_parser.get_shows_destination_path()
    source_path = arguments_parser.get_source_path()

    show_name = arguments_parser.get_show_name()
    if show_name:
        mover.move_episodes_by_name(show_name, episodes_destination_root, source_path)
        logger.log('Finished')
        return

    file_path = arguments_parser.get_file_path()
    if file_path:
        mover.move_media_by_path(file_path)
        logger.log('Finished')

    logger.log('No action was made')
