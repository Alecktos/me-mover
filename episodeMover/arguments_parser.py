import sys


def get_shows_destination_path():
    return __get_destination_path('-show-destination')

def get_movies_destination_path():
    return __get_destination_path('-movie-destination')

def __get_destination_path(destination_argument):
    destination_path = '.'
    if destination_argument in sys.argv:
        index = sys.argv.index(destination_argument)
        destination_path = sys.argv[index + 1]
    return destination_path


def get_source_path():
    source_path = '.'
    if '-source' in sys.argv:
        index = sys.argv.index('-source')
        source_path = sys.argv[index + 1]
    return source_path


def get_file_path():
    if '-file-name' not in sys.argv:
        return None
        #raise ArgumentParserException('-file-name needs to be set')

    index = sys.argv.index('-file-name')
    # if len(sys.argv) - 1 <= index :
    #     raise Exception('-file-name value needs to be set')

    return sys.argv[index+1]


def get_show_name():
    if '-show-name' not in sys.argv:
        return None
    #     raise ArgumentParserException('-show-name needs to be set')

    index = sys.argv.index('-show-name')
    # if len(sys.argv) - 1 <= index:
    #     raise Exception('-show-name value needs to be set')
    # todo validate when calling instead. Only one can be present. Borde inte var argument Borde vara kommandon!

    return sys.argv[index+1]


class ArgumentParserException(Exception):
    pass



