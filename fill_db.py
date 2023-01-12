import os

from database.db import DbMethods
from logs.exception import exception
from logs.logger import logger
from utils.helpers import handle_directories, handle_files, handle_last_slash
from utils.parser import args, parse_arguments


def populate_database(start_path: str, db: DbMethods) -> None:
    """
    This function iterates through all directories and files and writes
    data to the sqlite database in table directories with fields:
    id, parent_id, name
    and in table files with fields:
    id, directory_id, name, modified_date, permission, hash.

    :param start_path: str
        Path of directory
    :param db: DbMethods
        Class with methods for manipulate with db.
    :return: None
    """
    parent_id = "null"

    for dir_path, subdir_list, file_list in os.walk(start_path):
        directory_id = handle_directories(db=db, dir_path=dir_path,
                                          parent_id=parent_id)

        for filename in file_list:
            handle_files(db=db, dir_path=dir_path,
                         filename=filename, directory_id=directory_id)


@exception
def main():
    parse_arguments()
    path = handle_last_slash(args.directory)
    db = DbMethods(args.database)
    db.delete_tables_if_files_or_dir_not_exists()
    db.create_table_directories_if_not_exists()
    db.create_table_files_if_not_exists()
    populate_database(path, db)


if __name__ == "__main__":
    logger.info("Script start")
    main()
    logger.info("Script finished")
