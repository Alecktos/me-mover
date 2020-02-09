import logging

Log = logging.getLogger("me-mover")


def info(message):
    Log.info(message)


def debug(message):
    Log.debug(message)
