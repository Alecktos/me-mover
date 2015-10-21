import sys


def get_destination_path():
    destination_path = '.'
    if '-destination' in sys.argv:
        index = sys.argv.index('-destination')
        destination_path = sys.argv[index + 1]
    return destination_path


def get_source_path():
    source_path = '.'
    if '-source' in sys.argv:
        index = sys.argv.index('-source')
        source_path = sys.argv[index + 1]
    return source_path


def in_force_mode():
    force_create_folders = False
    if '-force' in sys.argv:
        force_create_folders = True

    return force_create_folders


def get_show_name():
    if '-show-name' not in sys.argv:
        raise ArgumentParserException('-show-name needs to be set')

    index = sys.argv.index('-show-name')
    if len(sys.argv) - 1 <= index:
        raise Exception('-show-name value needs to be set')

    return sys.argv[index+1]


class ArgumentParserException(Exception):
    pass



