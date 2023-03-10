import sqlite3
from sqlite3 import Cursor

from logs.logger import logger


def singleton(class_):
    """
    Singleton decorator for more effective using
    connection to db
    """
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class BaseDbHelper:
    """
    Base class for store connect, path and cursor
    """

    def __init__(self, path_to_db):
        self.path_to_db = path_to_db
        self._connect = self._get_connect()
        self.cursor = self._connect.cursor()

    def _get_connect(self) -> sqlite3.Connection:
        """
        Method for getting connect of db sqlite
        :return: sqlite3.Connection
        """
        try:
            connect = sqlite3.connect(self.path_to_db)
        except sqlite3.Error as e:
            logger.error("Error:", e)
        else:
            return connect

    def _execute_query(self, query: str) -> Cursor:
        """"
        Method for execute query and commit transaction
        """
        try:
            result = self.cursor.execute(query)
        except sqlite3.Error as e:
            logger.error(f"Error of execute, message: {e}")
        else:
            return result

    def _commit(self) -> None:
        """
        Method for commit transaction of executed
        :return: None
        """
        try:
            self._connect.commit()
        except sqlite3.Error as e:
            logger.error(f"Error of commit, message: {e}")


class DbHelper(BaseDbHelper):
    """
    Object for run low-level queries
    """

    def create_table(self, table_name: str,
                     fields: str) -> Cursor:
        result = self._execute_query(f"CREATE TABLE IF NOT EXISTS {table_name} "
                                     f"({fields})")
        return result

    def get_rows_from_table(self, table: str,
                            filters="", field="*") -> list:
        table = table
        filters = filters
        query = f"SELECT {field} FROM {table}"
        if len(filters) > 0:
            query += f" where {filters}"
        result = self._execute_query(query).fetchall()
        return result if len(result) > 0 else []

    def insert_row(self, table: str,
                   columns: str, values: str) -> Cursor:
        query = f"INSERT INTO {table} ({columns}) values ({values})"
        return self._execute_query(query)

    def delete_row(self, table: str,
                   filters: str):
        query = f"DELETE FROM {table} WHERE {filters}"
        self._execute_query(query)

    def select_join(self, fields: str,
                    left_table: str,
                    right_table: str,
                    on_fields: str,
                    filters: str) -> list:
        query = (f"SELECT {fields} "
                 f"FROM {left_table} "
                 f"JOIN {right_table} "
                 f"ON {on_fields} "
                 f"WHERE {filters}")
        result = self._execute_query(query).fetchall()
        return [i for i in result] if len(result) > 0 else []


@singleton
class DbMethods(DbHelper):
    """
    Object for run high-level queries
    """

    def create_table_directories_if_not_exists(self):
        self.create_table(table_name="directories",
                          fields="id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT")

    def create_table_files_if_not_exists(self):
        self.create_table(table_name="files",
                          fields="id INTEGER PRIMARY KEY, directory_id INTEGER, "
                                 "name TEXT, modified_date TEXT, permission INTEGER, "
                                 "hash TEXT")

    def add_row_to_dir(self, parent_id: str, name: str) -> Cursor:
        row = self.insert_row(table="directories",
                              columns="parent_id, name",
                              values=f"{parent_id}, '{name}'")
        return row

    def add_row_to_file(self, directory_id: int,
                        name: str, modified_date: str, permission: int, file_hash: str) -> None:
        self.insert_row(table="files",
                        columns="directory_id, name, modified_date, permission, hash",
                        values=f"{directory_id}, '{name}', '{modified_date}', {permission}, '{file_hash}'")

    def file_is_present(self, name: str,
                        file_hash: str) -> bool:
        row = self.get_rows_from_table(table="files",
                                       filters=f"name = '{name}' "
                                               f"AND hash = '{file_hash}'")
        return bool(row)

    def dir_is_present(self, name: str) -> bool:
        row = self.get_rows_from_table(table="directories",
                                       filters=f"name = '{name}'")
        return bool(row)

    def delete_table(self, table_name: str) -> None:
        self._execute_query(f"DROP TABLE IF EXISTS {table_name}; ")

    def delete_tables_if_files_or_dir_not_exists(self) -> None:
        self._execute_query("SELECT name FROM sqlite_master WHERE type='table' "
                            "AND name='files' OR name='directories';")
        if self.cursor.fetchone() is not None:
            self._execute_query("DROP TABLE files;")
            self._execute_query("; DROP TABLE directories;")
            logger.info("Tables 'files' and 'directories' have been dropped.")

    def get_dir_id_by_name(self, name: str) -> int:
        row = self.get_rows_from_table(table="directories",
                                       filters=f"name = '{name}'",
                                       field="id")[0][0]
        return row

