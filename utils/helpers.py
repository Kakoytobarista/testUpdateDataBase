import datetime
import os

from py_essentials import hashing as hs

from database.db import DbMethods
from logs.logger import logger


def handle_last_slash(path: str) -> str:
    """
    Function for delete last slash
    """
    result_path = path[:-1] if path.endswith("/") else path
    return result_path


def handle_directories(db: DbMethods, dir_path: str, parent_id: str):
    """
    Function for handle directory and write data into database
    :param db: DbMethods
        Instance of class DbMethods for interacting with db
    :param dir_path: string
        Path string of directory path
    :param parent_id: Union[str, int]
        Id of parent_id directory
    :return: directory_id, its param for table files
    """
    if not db.dir_is_present(name=dir_path):
        parent_dir_path = os.path.dirname(dir_path)
        if db.dir_is_present(name=parent_dir_path):
            parent_id = db.get_dir_id_by_name(parent_dir_path)

        directory_id = db.add_row_to_dir(parent_id=parent_id, name=dir_path).lastrowid
        logger.info(f"Write to directory table::  Dirname : {dir_path.split('/')[-1]}"
                    f" :: Path: {dir_path}")
        return directory_id


def handle_files(db, dir_path, filename, directory_id):
    """
    Function for handle files and write data of files into database
    :param db: DbMethods
        Instance of class DbMethods for interacting with db
    :param dir_path: string
        Path string of directory path
    :param filename: string
        Name of file name
    :param directory_id: Union[id, str]
        its param for table files
    :return: None
    """
    path = os.path.join(dir_path, filename)
    file_hash = hs.fileChecksum(path, "sha256")
    if not db.file_is_present(name=filename, file_hash=file_hash):
        last_modified = datetime.datetime.fromtimestamp(os.stat(path).st_mtime)
        permissions = os.stat(path).st_mode
        db.add_row_to_file(directory_id=directory_id, name=filename,
                           modified_date=last_modified, permission=permissions,
                           file_hash=file_hash)
        logger.info(f"Write to File table:: Filename: {filename} :: Path: {path}"
                    f" :: modified: {last_modified} :: "
                    f"Permissions: {permissions} :: Hash: {file_hash}")
