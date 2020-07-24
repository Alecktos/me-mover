import os
import shutil


def delete_file(path):
    os.remove(path)


def create_file(path):
    if not os.path.exists(get_parent(path)):
        os.makedirs(get_parent(path))
    fd = os.open(path, os.O_CREAT)
    os.close(fd)


def file_exist(file_path):
    return os.path.isfile(file_path)


def directory_exist(directory_path):
    return os.path.isdir(directory_path)


def move(source, destination):
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


def get_biggest_files(dir_path, root_path):
    # traverse up a folder structure. Finding the biggest file
    while True:
        biggest_file = get_biggest_file(dir_path)

        if biggest_file.exist():
            yield biggest_file

        if dir_path.strip('/') == root_path.strip('/'):
            break

        dir_path = get_parent(dir_path)


def get_biggest_file(dir_path):
    class BiggestFile:
        def __init__(self):
            self.size = -1
            self.path = None

        def exist(self):
            return self.size != -1

    biggest_file = BiggestFile()

    for file in get_directory_content(dir_path):
        file = dir_path + '/' + file
        if path_is_directory(file):
            continue
        file_size = get_file_size(file)
        if biggest_file.size < file_size:
            biggest_file.size = get_file_size(file)
            biggest_file.path = file

    return biggest_file


def get_files(path):
    if not path_is_directory(path):
        yield path
        return

    for root, dirs, files in os.walk(path):
        for name in files:
            yield root + '/' + name


def path_is_directory(path):
    return os.path.isdir(path)


def get_file_type(path):
    return os.path.splitext(path)[1]


def get_last_path_part(path):
    if not path:
        return path

    if path[-1] == '/':
        path = path[:-1]
    return os.path.basename(path)


def get_last_name_from_path(path):
    path_removed_extension = get_path_without_extension(path)
    return get_last_path_part(path_removed_extension)


def get_path_without_extension(path):
    if path_is_directory(path):
        return path
    return os.path.splitext(path)[0]


# Get the file's parent directory
def get_parent(path):
    return os.path.dirname(path)


def get_file_size(path):
    return os.path.getsize(path)


class PathIsNotDirectoryException(Exception):

    def __init__(self, path):
        super(PathIsNotDirectoryException, self).__init__(path + ' is not a directory')