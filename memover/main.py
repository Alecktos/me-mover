import asyncio

from memover.watcher import async_watcher
from . import arguments_parser, logger
from . import mover


def main():
    args = arguments_parser.get_args()
    if not args:
        return

    logger.setup(args.log_level)

    if args.type == arguments_parser.Commands.BY_NAME:
        mover.move_media_by_name(
            args.media_name,
            args.source,
            args.show_destination,
            args.movie_destination
        )
        return

    if args.type == arguments_parser.Commands.BY_PATH:
        mover.move_media_by_path(
            args.source,
            args.show_destination,
            args.movie_destination
        )
        return

    if args.type == arguments_parser.Commands.WATCH:
        asyncio.run(async_watcher.run(args))
        return
