import shutil
import os


def delete_file(self, path):
    os.remove(path)

def create_file(self, path):
    os.open(path, os.O_CREAT)

def check_file_existance(self, file_path):
    return os.path.isfile(file_path)

def check_directory_existance(self, directory_path):
    return os.path.isdir(directory_path)

def move_file(self, source, destination):
    os.rename(source, destination)

def create_dir(self, directory_path):
    os.makedirs(directory_path)

def delete_directory(self, directory_path):
    shutil.rmtree(directory_path)

def get_subdirectories(self, directory_path):
    return os.listdir(directory_path)