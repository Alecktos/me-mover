import asyncio
import logging

from memover.watcher import async_watcher
from . import arguments_parser
from . import mover


def main():
    args = arguments_parser.get_args()
    if not args:
        return

    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")

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
