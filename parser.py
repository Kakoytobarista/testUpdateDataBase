import argparse
import os
import sys

from utils.exceptions import DataBaseAccessDeniedException, RootDirAccessDeniedException
from logs.logger import logger
from logs.exception import exception

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument("-d", "--directory", help="Root directory", required=True)
parser.add_argument("-b", "--database", help="Path to database", required=True)
parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
parser.add_argument("-l", "--log", help="Logging events", action="store_true")
parser.add_argument("-h", "--short-help", action="store_true", help="show short help")
parser.add_argument("--help", action="store_true", help="show extended help")
args = parser.parse_args()


@exception
def parse_arguments():
    logger.info(f"Parsed args: {args}")
    if args.verbose:
        logger.debug("Verbose argument is given")

    if args.log:
        logger.debug("Log argument is given")

    if not args.directory:
        logger.error("You are dont write a root directory")

    if not args.database:
        logger.error("You are dont write a database directory")

    if not os.path.exists(args.directory):
        logger.error("Root directory doesn't exist")
        sys.exit(1)

    if not os.path.exists(args.database):
        logger.error("Database path doesn't exist")
        sys.exit(1)

    try:
        os.access(args.directory, os.W_OK)
    except RootDirAccessDeniedException as e:
        logger.error(f"Root directory is not accessible, {e}")
        sys.exit(1)

    try:
        os.access(args.database, os.W_OK)
    except DataBaseAccessDeniedException as e:
        logger.error(f"Database path is not accessible, {e}")
        sys.exit(1)
