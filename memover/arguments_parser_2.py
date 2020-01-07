import argparse
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
            auto_quit: int = None,
            media_name: str = None
    ):
        self.__type = type
        self.__source = source
        self.__show_destination = show_destination
        self.__movie_destination = movie_destination
        self.__media_name = media_name
        self.__quit = auto_quit
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
    def quit(self) -> int:
        return self.__quit

    @property
    def media_name(self) -> str:
        return self.__media_name

    def __str__(self) -> str:
        return f'type: {self.__type}, source: {self.__source}, show_destination: {self.__show_destination}, movie_destination: {self.__movie_destination}, quit: {self.__quit}, media_name: {self.__media_name}'


class MeMoverArgsCreator:

    current_args = None

    def name(self, args):
        self.current_args = MeMoverArgs(Commands.BY_NAME, args.source, args.show_destination, args.movie_destination, None, args.media_name)

    def path(self, args):
        self.current_args = MeMoverArgs(Commands.BY_PATH, args.source, args.show_destination, args.movie_destination)

    def watch(self, args):
        self.current_args = MeMoverArgs(Commands.WATCH, args.source, args.show_destination, args.movie_destination, args.quit)

    def add_common_arguments(self, parser):
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

    def create_name(self, subparsers):
        parser_name = subparsers.add_parser('by-name')
        parser_name.add_argument(
            'media_name',
            metavar='name',
            help='name of show or movie to move'
        )
        parser_name.add_argument(
            'source',
            metavar='source',
            help='source directory to look for media in'
        )
        self.add_common_arguments(parser_name)
        parser_name.set_defaults(func=self.name)

    def create_path(self, subparsers):
        parser_path = subparsers.add_parser('by-path')
        parser_path.add_argument(
            'source',
            metavar='source',
            help='source path of movie or tv-show to move'
        )
        self.add_common_arguments(parser_path)

        parser_path.set_defaults(func=self.path)

    def create_watch(self, subparsers):
        parser_watch = subparsers.add_parser('watch')
        parser_watch.add_argument(
            'source',
            metavar='source',
            help='source directory to to watch for incoming tv-shows or movies'
        )
        self.add_common_arguments(parser_watch)
        parser_watch.add_argument('--quit', '-q', type=int, required=False, dest='quit', help='Number of seconds until exit')
        parser_watch.set_defaults(func=self.watch)


def get_args():
    me_mover_args_creator = MeMoverArgsCreator()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="commands")

    me_mover_args_creator.create_name(subparsers)
    me_mover_args_creator.create_path(subparsers)
    me_mover_args_creator.create_watch(subparsers)

    args = parser.parse_args()
    args.func(args)

    return me_mover_args_creator.current_args
