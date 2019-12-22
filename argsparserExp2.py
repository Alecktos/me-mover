import argparse
import os


class readable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


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

    def __init__(self, type, source, show_destination, movie_destination):
        self.type = type
        self.source = source
        self.show_destination = show_destination
        self.movie_destination = movie_destination
        super().__init__()

    def __str__(self) -> str:
        return f'type: {self.type}, source: {self.source}, show_destination: {self.show_destination}, movie_destination: {self.movie_destination}, quit {self.quit}'


class MeMoverArgsCreator:

    current_args = None

    def name(self, args):
        self.current_args = MeMoverArgs(Commands.BY_NAME, args.source, args.show_destination, args.movie_destination)
        print(self.current_args)
        # print("you screamed "+' '.join(args.words))

    def count(self, args):
        print("you counted to {0}".format(args.count))

    def add_common_arguments(self, parser):
        parser.add_argument(
            'source',
            metavar='source',
            # action=readable_dir,
            help='source directory to look for media in'
        )
        parser.add_argument(
            'show_destination',
            # action=readable_dir,
            metavar='shows-destination',
            help='root show destination directory'
        )
        parser.add_argument(
            'movie_destination',
            # action=readable_dir,
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

        parser_path.set_defaults(func=self.count)

    def createWatch(self, subparsers):
        parser_watch = subparsers.add_parser('watch')
        self.add_common_arguments(parser_watch)
        # custom
        parser_watch.add_argument('--quit', '-q', type=int, required=False, dest='quit', help='Number of seconds until exit')


def init():
    me_mover_args_creator = MeMoverArgsCreator()

    parser = argparse.ArgumentParser()

    #tell the parser that there will be subparsers
    subparsers = parser.add_subparsers(help="commands")

    # todo: testa så alla kommandon fungerar.

    me_mover_args_creator.createName(subparsers)
    me_mover_args_creator.createPath(subparsers)
    me_mover_args_creator.createWatch(subparsers)

    #parse the args
    args = parser.parse_args()
    args.func(args)  #args.func is the function that was set for the particular subparser

    # should print with all configurations
    print(str(me_mover_args_creator.current_args))


init()