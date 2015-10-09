import sys
from file_matcher import FileMatcher
from file_mover import FileMover

__author__ = 'alexander.persson'


def main():
    show_name = sys.argv[1]
    file_matcher = FileMatcher()
    file_paths = file_matcher.search_files(show_name, 'testfolder/') # TODO: search files borde det vara

    file_mover = FileMover()
    file_mover.move_files(file_paths, 'destination', show_name) #TODO: borde vara move_files

