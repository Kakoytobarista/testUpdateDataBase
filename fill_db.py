import datetime
import os
from parser import args, parse_arguments

from py_essentials import hashing as hs

from database.db import DbMethods
from logs.exception import exception
from logs.logger import logger


def populate_database(start_path: str, db) -> None:
    parent_id = "null"

    for dir_path, subdir_list, file_list in os.walk(start_path):
        dir_name = dir_path.split("/")[-1] if dir_path[-1] != "/" else dir_path.split("/")[-2]
        if not db.dir_is_present(name=dir_path):
            db.add_row_to_dir(parent_id=parent_id, name=dir_path)
            dir_id = db.cursor.lastrowid
            parent_id = dir_id
            logger.info(f"Dirname: {dir_name} :: Path: {dir_path}")

        for filename in file_list:
            path = os.path.join(dir_path, filename)
            hash_ = hs.fileChecksum(path, "sha256")
            if db.file_is_present(name=filename):
                continue

            last_modified = datetime.datetime.fromtimestamp(os.stat(path).st_mtime)
            permissions = os.stat(path).st_mode
            db.add_row_to_file(directory_id=parent_id, name=filename,
                               modified_date=last_modified, permission=permissions,
                               file_hash=hash_)
            logger.info(f"Filename: {filename} :: Path: {path} :: modified: {last_modified} :: "
                        f"Permissions: {permissions} :: Hash: {hash_}")


@exception
def main():
    parse_arguments()
    db = DbMethods(args.database)
    db.delete_tables_if_files_or_dir_not_exists()
    db.create_table_directories_if_not_exists()
    db.create_table_files_if_not_exists()
    db.delete_args_related_rows(args.directory)
    populate_database(args.directory, db)


if __name__ == "__main__":
    logger.info("Script start")
    main()
    logger.info("Script finished")
