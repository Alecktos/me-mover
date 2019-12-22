import argparse

# TODO 1
# parser = argparse.ArgumentParser(description='Move movies and tv-shows in a specified file structure.')
#
# parser.add_argument('--path', type=str, help='path to movie or tv-show to be moved')
# parser.add_argument('--name', type=str, help='Move all movies and/or tv-shows with a certain name')
#
# args = parser.parse_args()
#
# print(args.indir)

# TODO 2
# parent_parser = argparse.ArgumentParser(add_help=False)
#
# parent_parser.add_argument('--user', '-u',
#                            default='nothing',
#                            help='username')
# parent_parser.add_argument('--debug', default=False, required=False,
#                            action='store_true', dest="debug", help='debug flag')
# main_parser = argparse.ArgumentParser()
#
# service_subparsers = main_parser.add_subparsers(title="service",
#                                                 dest="service_command")
# service_parser = service_subparsers.add_parser("first", help="first",
#                                                parents=[parent_parser])
#
# action_subparser = service_parser.add_subparsers(title="action",
#                                                  dest="action_command")
# action_parser = action_subparser.add_parser("second", help="second",
#                                             parents=[parent_parser])
#
# args = main_parser.parse_args()

# TODO 3

# import sys
#
#
# class FakeGit(object):
#
#     def __init__(self):
#         parser = argparse.ArgumentParser(
#             description='Pretends to be git',
#             usage='''git <command> [<args>]
#
# The most commonly used git commands are:
#    commit     Record changes to the repository
#    fetch      Download objects and refs from another repository
# ''')
#         parser.add_argument('command', help='Subcommand to run')
#         # parse_args defaults to [1:] for args, but you need to
#         # exclude the rest of the args too, or validation will fail
#         args = parser.parse_args(sys.argv[1:2])
#         if not hasattr(self, args.command):
#             print('Unrecognized command')
#             parser.print_help()
#             exit(1)
#         # use dispatch pattern to invoke method with same name
#         getattr(self, args.command)()
#
#     def commit(self):
#         parser = argparse.ArgumentParser(
#             description='Record changes to the repository')
#         # prefixing the argument with -- means it's optional
#         parser.add_argument('--amend', action='store_true')
#         # now that we're inside a subcommand, ignore the first
#         # TWO argvs, ie the command (git) and the subcommand (commit)
#         args = parser.parse_args(sys.argv[2:])
#         print('Running git commit, amend=%s' % args.amend)
#
#     def fetch(self):
#         parser = argparse.ArgumentParser(
#             description='Download objects and refs from another repository')
#         # NOT prefixing the argument with -- means it's not optional
#         parser.add_argument('repository')
#         args = parser.parse_args(sys.argv[2:])
#         print('Running git fetch, repository=%s' % args.repository)
#
#
# if __name__ == '__main__':
#     FakeGit()

# TODO 4
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

__current_args = None


class Commands:
    BY_NAME = 'by-name'
    BY_PATH = 'by-path'
    WATCH = 'watch'


class MeMoverArgs:
    type = None
    source = None
    show_destination = None
    movie_destination = None

    def __init__(self, type, source, show_destination, movie_destination):
        self.type = type
        self.source = source
        self.show_destination = show_destination
        self.movie_destination = movie_destination
        super().__init__()


def name(args):
    __current_args = MeMoverArgs(Commands.BY_NAME, args.source, args['show-destination'], )
    # print("you screamed "+' '.join(args.words))


def count(args):
    print("you counted to {0}".format(args.count))

def createName(subparsers):
    #Add parsers to the object that was returned by `add_subparsers`
    parser_name = subparsers.add_parser('by-name')

    #use that as you would any other argument parser parser_name.add_argument('source', action=readable_dir, help='source directory to look for media in')
    parser_name.add_argument('show-destination', action=readable_dir, help='show destination directory')
    parser_name.add_argument('movie-destination', action=readable_dir, help='movie destination directory')

    #set_defaults is nice to call a function which is specific to each subparser
    parser_name.set_defaults(func=name)


def createPath(subparsers):
    parser_path = subparsers.add_parser('by-path')
    parser_path.add_argument('source', action=readable_dir, help='source directory to look for media in')
    parser_path.add_argument('show-destination', action=readable_dir, help='show destination directory')
    parser_path.add_argument('movie-destination', action=readable_dir, help='movie destination directory')

    parser_path.set_defaults(func=count)


def createWatch(subparsers):
    parser_path = subparsers.add_parser('watch')
    parser_path.add_argument('source', action=readable_dir, help='source directory to look for media in')
    parser_path.add_argument('show-destination', action=readable_dir, help='show destination directory')
    parser_path.add_argument('movie-destination', action=readable_dir, help='movie destination directory')

    # custom
    parser_path.add_argument('--quit', type=int, required=False, help='Number of seconds until exit')

    # parent_parser.add_argument('--debug', default=False, required=False,
#                            action='store_true', dest="debug", help='debug flag')


def get_arguments():
    parser = argparse.ArgumentParser()

    #tell the parser that there will be subparsers
    subparsers = parser.add_subparsers(help="commands")

    createName(subparsers)
    createPath(subparsers)
    createWatch(subparsers)

    #parse the args
    args = parser.parse_args()
    args.func(args)  #args.func is the function that was set for the particular subparser