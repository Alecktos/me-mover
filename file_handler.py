import shutil
import os


class FileHandler(object):

    def delete_file(self, path):
        os.remove(path)

    def create_file(self, path):
        os.open(path, os.O_CREAT)

    def check_file_existance(self, file_path):
        return os.path.isfile(file_path)

    def move_file(self, source, destination):
        os.rename(source, destination)

    def create_dir(self, directory_path):
        os.makedirs(directory_path)

    def delete_directory(self, directory_path):
        shutil.rmtree(directory_path)
