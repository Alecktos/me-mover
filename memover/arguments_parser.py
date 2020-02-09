import argparse
import logging
from enum import Enum


class Commands(Enum):
    BY_NAME = 1
    BY_PATH = 2
    WATCH = 3


class MeMoverArgs:
    def __init__(
            self,
            type: Commands,
            source: str,
            show_destination: str,
            movie_destination: str,
            log_level: int,
            auto_quit: int = None,
            media_name: str = None
    ):
        self.__type = type
        self.__source = source
        self.__show_destination = show_destination
        self.__movie_destination = movie_destination
        self.__media_name = media_name
        self.__quit = auto_quit
        self.__log_level = log_level
        super().__init__()

    @property
    def type(self) -> Commands:
        return self.__type

    @property
    def source(self) -> str:
        return self.__source

    @property
    def show_destination(self) -> str:
        return self.__show_destination

    @property
    def movie_destination(self) -> str:
        return self.__movie_destination

    @property
    def log_level(self) -> int:
        return self.__log_level

    @property
    def quit(self) -> int:
        return self.__quit

    @property
    def media_name(self) -> str:
        return self.__media_name

    def __str__(self) -> str:
        return f'type: {self.__type}, source: {self.__source}, show_destination: {self.__show_destination}, movie_destination: {self.__movie_destination}, lifetime: {self.__quit}, media_name: {self.__media_name}'


class MeMoverArgsCreator:

    def __init__(self):
        self.__args = None

    def generate_args(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help="commands")

        self.__create_name(subparsers)
        self.__create_path(subparsers)
        self.__create_watch(subparsers)

        args = parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()

    @property
    def args(self):
        return self.__args

    def __set_to_name(self, args):
        self.__args = MeMoverArgs(Commands.BY_NAME, args.source, args.show_destination, args.movie_destination, args.verbose, None, args.media_name)

    def __set_to_path(self, args):
        self.__args = MeMoverArgs(Commands.BY_PATH, args.source, args.show_destination, args.movie_destination, args.verbose)

    def __set_to_watch(self, args):
        self.__args = MeMoverArgs(Commands.WATCH, args.source, args.show_destination, args.movie_destination, args.verbose, args.quit)

    def __create_name(self, subparsers):
        parser_name = subparsers.add_parser('by-name')
        parser_name.add_argument(
            'media_name',
            metavar='name',
            help='name of TV show or movie to move'
        )
        parser_name.add_argument(
            'source',
            metavar='source',
            help='source directory to look for media in'
        )
        self.__add_common_arguments(parser_name)
        parser_name.set_defaults(func=self.__set_to_name)

    def __create_path(self, subparsers):
        parser_path = subparsers.add_parser('by-path')
        parser_path.add_argument(
            'source',
            metavar='source',
            help='source path of movie or tv-show to move'
        )
        self.__add_common_arguments(parser_path)

        parser_path.set_defaults(func=self.__set_to_path)

    def __create_watch(self, subparsers):
        parser_watch = subparsers.add_parser('watch')
        parser_watch.add_argument(
            'source',
            metavar='source',
            help='source directory to to watch for incoming TV shows and movies'
        )
        self.__add_common_arguments(parser_watch)
        parser_watch.add_argument('--lifetime', type=int, required=False, dest='quit', help='Number of seconds until exit')
        parser_watch.set_defaults(func=self.__set_to_watch)

    @staticmethod
    def __add_common_arguments(parser):
        parser.add_argument(
            'show_destination',
            metavar='shows-destination',
            help='show destination directory'
        )
        parser.add_argument(
            'movie_destination',
            metavar='movies-destination',
            help='movie destination directory'
        )

        parser.add_argument(
            "-v", "--verbose",
            help="Increase output verbosity",
            action="store_const",
            const=logging.DEBUG,
            default=logging.INFO
        )

me_mover_args_creator = MeMoverArgsCreator()


def get_args() -> MeMoverArgs:
    if not me_mover_args_creator.args:
        me_mover_args_creator.generate_args()
    return me_mover_args_creator.args


if __name__ == '__main__':
    current_args = get_args()
    print(current_args)
