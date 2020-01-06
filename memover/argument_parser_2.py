import argparse


class Commands:
    BY_NAME = 'by-name'
    BY_PATH = 'by-path'
    WATCH = 'watch'


class MeMoverArgs:
    type = None
    source = None
    show_destination = None
    movie_destination = None
    quit = None

    def __init__(self, type, source, show_destination, movie_destination, auto_quit=None):
        self.type = type
        self.source = source
        self.show_destination = show_destination
        self.movie_destination = movie_destination
        self.quit = auto_quit
        super().__init__()

    def __str__(self) -> str:
        return f'type: {self.type}, source: {self.source}, show_destination: {self.show_destination}, movie_destination: {self.movie_destination}, quit {self.quit}'


class MeMoverArgsCreator:

    current_args = None

    def name(self, args):
        self.current_args = MeMoverArgs(Commands.BY_NAME, args.source, args.show_destination, args.movie_destination)

    def path(self, args):
        self.current_args = MeMoverArgs(Commands.BY_PATH, args.source, args.show_destination, args.movie_destination)

    def watch(self, args):
        self.current_args = MeMoverArgs(Commands.WATCH, args.source, args.show_destination, args.movie_destination, args.quit)

    def add_common_arguments(self, parser):
        parser.add_argument(
            'source',
            metavar='source',
            help='source directory to look for media in'
        )
        parser.add_argument(
            'show_destination',
            metavar='shows-destination',
            help='root show destination directory'
        )
        parser.add_argument(
            'movie_destination',
            metavar='movies-destination',
            help='root movie destination directory'
        )

    def createName(self, subparsers):
        #Add parsers to the object that was returned by `add_subparsers`
        parser_name = subparsers.add_parser('by-name')
        self.add_common_arguments(parser_name)

        #set_defaults is nice to call a function which is specific to each subparser
        parser_name.set_defaults(func=self.name)

    def createPath(self, subparsers):
        parser_path = subparsers.add_parser('by-path')
        self.add_common_arguments(parser_path)

        parser_path.set_defaults(func=self.path)

    def createWatch(self, subparsers):
        parser_watch = subparsers.add_parser('watch')
        self.add_common_arguments(parser_watch)
        parser_watch.add_argument('--quit', '-q', type=int, required=False, dest='quit', help='Number of seconds until exit')
        parser_watch.set_defaults(func=self.watch)


def get_current_args():
    me_mover_args_creator = MeMoverArgsCreator()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="commands")

    me_mover_args_creator.createName(subparsers)
    me_mover_args_creator.createPath(subparsers)
    me_mover_args_creator.createWatch(subparsers)

    args = parser.parse_args()
    args.func(args)

    return me_mover_args_creator.current_args
