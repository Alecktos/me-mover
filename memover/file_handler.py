import shutil
import os


def delete_file(path):
    os.remove(path)


def create_file(path):
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


def get_directory_content(directory_path):
    if not path_is_directory(directory_path):
        raise PathIsNotDirectoryException(directory_path)

    return os.listdir(directory_path)


def path_is_directory(path):
    return os.path.isdir(path)


def get_file_type(path):
    return os.path.splitext(path)[1]


def get_last_path_part(path):
    return os.path.basename(path)


class PathIsNotDirectoryException(Exception):

    def __init__(self, path):
        super(PathIsNotDirectoryException, self).__init__(path + ' is not a directory')