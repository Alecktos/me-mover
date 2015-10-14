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
    os.rename(source, destination)


def create_dir(directory_path):
    os.makedirs(directory_path)


def delete_directory(directory_path):
    shutil.rmtree(directory_path)


def get_subdirectories(directory_path):
    return os.listdir(directory_path)