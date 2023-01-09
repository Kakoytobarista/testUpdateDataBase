import logging
import sys


def create_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

    handler = logging.FileHandler("my_log.log")
    console_handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(formatter)
    console_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))

    logger.addHandler(console_handler)
    logger.addHandler(handler)
    return logger


logger = create_logger()
