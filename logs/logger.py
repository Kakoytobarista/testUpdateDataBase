import logging
import sys

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")


def create_logger() -> logging.getLogger():
    """
    Function for getting logger
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    logger.setLevel(logging.INFO)
    return logger


def add_write_log_handler(logger_obj: logging.getLogger()):
    """
    Function for add FileHandler
    :param logger_obj: logging.getLogger()
    :return: None
    """
    handler = logging.FileHandler("my_log.log")
    handler.setFormatter(formatter)
    logger_obj.addHandler(handler)


def add_stream_handler(logger_obj: logging.getLogger()) -> None:
    """
    Function for add StreamHandler
    :param logger_obj: logging.getLogger()
    :return: None
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger_obj.addHandler(console_handler)


logger = create_logger()
