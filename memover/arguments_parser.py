import sys


class Commands:
    NAME = 'name'
    FILE = 'file'


class Arguments:
    SHOW_DESTINATION = '-show-destination'
    MOVIE_DESTINATION = '-movie-destination'
    SOURCE = '-source'
    NAME = '-name'
    FILE_PATH = '-file-path'


def get_shows_destination_path():
    return __get_destination_path(Arguments.SHOW_DESTINATION)


def get_movies_destination_path():
    return __get_destination_path(Arguments.MOVIE_DESTINATION)


def __get_destination_path(destination_argument):
    destination_path = None
    if destination_argument in sys.argv:
        index = sys.argv.index(destination_argument)
        destination_path = sys.argv[index + 1]
    return destination_path


def get_show_source_path():
    source_path = '.'
    if Arguments.SOURCE in sys.argv:
        index = sys.argv.index(Arguments.SOURCE)
        source_path = sys.argv[index + 1]
    return source_path


def get_file_path():
    if Arguments.FILE_PATH not in sys.argv:
        return None

    index = sys.argv.index(Arguments.FILE_PATH)
    return sys.argv[index+1]


def get_show_name():
    if Arguments.NAME not in sys.argv:
        return None

    index = sys.argv.index(Arguments.NAME)
    return sys.argv[index+1]


def get_command():
    if len(sys.argv) < 2:
        return None

    if sys.argv[1] == Commands.NAME or sys.argv[1] == Commands.FILE:
        return sys.argv[1]
    return None

