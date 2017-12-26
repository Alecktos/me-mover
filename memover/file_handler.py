import shutil
import os


def delete_file(path):
    os.remove(path)


def create_file(path):
    if not os.path.exists(get_parent(path)):
        os.makedirs(get_parent(path))
    os.open(path, os.O_CREAT)


def check_file_existance(file_path):
    return os.path.isfile(file_path)


def check_directory_existance(directory_path):
    return os.path.isdir(directory_path)


def move_file(source, destination):
    shutil.move(source, destination)


def create_dir(directory_path):
    os.makedirs(directory_path)


def delete_directory(directory_path):
    shutil.rmtree(directory_path)


def directory_is_empty(directory_path):
    return not get_directory_content(directory_path)


def get_directory_content(directory_path):
    if not path_is_directory(directory_path):
        raise PathIsNotDirectoryException(directory_path)

    return os.listdir(directory_path)


def get_files(directory_path):
    if not path_is_directory(directory_path):
        raise PathIsNotDirectoryException(directory_path)

    for root, dirs, files in os.walk(directory_path):
        for name in files:
            yield root + '/' + name


def path_is_directory(path):
    return os.path.isdir(path)


def get_file_type(path):
    return os.path.splitext(path)[1]


def get_last_path_part(path):
    return os.path.basename(path)


def get_last_name_from_path(path):
    path_removed_extension = get_path_without_extension(path)
    return get_last_path_part(path_removed_extension)


def get_path_without_extension(path):
    if path_is_directory(path):
        return path
    return os.path.splitext(path)[0]


def get_parent(path):
    return os.path.dirname(path)


def get_file_size(path):
    return os.path.getsize(path)


class PathIsNotDirectoryException(Exception):

    def __init__(self, path):
        super(PathIsNotDirectoryException, self).__init__(path + ' is not a directory')