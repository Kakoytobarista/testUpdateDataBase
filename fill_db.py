import os

from utils.helpers import handle_last_slash, handle_directories, handle_files
from utils.parser import args, parse_arguments


from database.db import DbMethods
from logs.exception import exception
from logs.logger import logger


def populate_database(start_path: str, db: DbMethods) -> None:
    parent_id = "null"

    for dir_path, subdir_list, file_list in os.walk(start_path):
        directory_id = handle_directories(db=db, dir_path=dir_path,
                                          parent_id=parent_id)

        for filename in file_list:
            handle_files(db=db, dir_path=dir_path, filename=filename,
                         directory_id=directory_id)


@exception
def main():
    parse_arguments()
    path = handle_last_slash(args.directory)
    db = DbMethods(args.database)
    db.delete_tables_if_files_or_dir_not_exists()
    db.create_table_directories_if_not_exists()
    db.create_table_files_if_not_exists()
    db.delete_args_related_rows(path)
    populate_database(path, db)


if __name__ == "__main__":
    logger.info("Script start")
    main()
    logger.info("Script finished")
