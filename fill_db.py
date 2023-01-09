import datetime
import os

from py_essentials import hashing as hs

from database.db import DbMethods
from logs.exception import exception
from logs.logger import logger
from parser import parse_arguments, args


def populate_database(start_path):
    db = DbMethods(args.database)
    parent_id = 'null'

    for dir_name, subdir_list, file_list in os.walk(start_path):
        db.add_row_to_dir(parent_id=parent_id, name=dir_name)
        dir_id = db.cursor.lastrowid
        parent_id = dir_id
        logger.info(f"Dirname: {dir_name} :: Parent Id: {parent_id}")

        for filename in file_list:
            path = os.path.join(dir_name, filename)
            last_modified = datetime.datetime.fromtimestamp(os.stat(path).st_mtime)
            permissions = os.stat(path).st_mode
            hash_ = hs.fileChecksum(path, "sha256")

            db.add_row_to_file(directory_id=parent_id, name=filename,
                               modified_date=last_modified, permission=permissions,
                               file_hash=hash_)
            logger.info(f"Filename: {filename} :: Path: {path} :: modified: {last_modified} :: "
                        f"Permissions: {permissions} :: Hash: {hash_}")


@exception
def main():
    parse_arguments()
    populate_database(args.directory)


if __name__ == "__main__":
    logger.info("Script start")
    main()
    logger.info("Script finished")
