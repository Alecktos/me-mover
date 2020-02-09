import logging

Log = logging.getLogger("me-mover")


def setup(level: int):
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")

    logging.getLogger('watchdog').setLevel(logging.INFO)


def info(message):
    Log.info(message)


def debug(message):
    Log.debug(message)
