import argparse
import os
import sys

from logs.exception import exception
from logs.logger import add_stream_handler, add_write_log_handler, logger
from utils.exceptions import (DataBaseAccessDeniedException,
                              RootDirAccessDeniedException)

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument("-h", "--short-help", action="help", help="show short help")
parser.add_argument("--help", action="help", help="show extended help")
parser.add_argument("-d", "--directory", help="Root directory", required=True)
parser.add_argument("-b", "--database", help="Path to database", required=True)
parser.add_argument("-l", "--log", help="Logging events", required=True)
parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
args = parser.parse_args()


@exception
def parse_arguments() -> None:
    """Function parser for handle args of script"""
    logger.info(f"Parsed args: {args}")
    add_write_log_handler(logger)

    if args.verbose:
        add_stream_handler(logger)
        logger.debug("Verbose argument is given")

    if not os.path.exists(args.directory):
        add_stream_handler(logger)
        logger.error("Root directory doesn't exist")
        sys.exit(1)

    if not os.path.exists(args.log):
        add_stream_handler(logger)
        logger.error("Log file doesn't exist")
        sys.exit(1)

    if not os.path.exists(args.database):
        add_stream_handler(logger)
        logger.error("Database path doesn't exist")
        sys.exit(1)

    try:
        os.access(args.directory, os.W_OK)
    except RootDirAccessDeniedException as e:
        add_stream_handler(logger)
        logger.error(f"Root directory is not accessible, {e}")
        sys.exit(1)

    try:
        os.access(args.database, os.W_OK)
    except DataBaseAccessDeniedException as e:
        add_stream_handler(logger)
        logger.error(f"Database path is not accessible, {e}")
        sys.exit(1)
