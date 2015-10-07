import sys

__author__ = 'alexander.persson'

from file_matcher import FileMatcher
from file_mover import FileMover

def main():
    show_name = sys.argv[1]
    file_matcher = FileMatcher()
    file_path = file_matcher.search_file(show_name, 'testfolder/')

    file_mover = FileMover()
    file_mover.move_file(file_path, 'destination', show_name)


# if __name__ == '__main__':
#     main()
