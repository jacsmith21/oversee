import logging


def factory(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
