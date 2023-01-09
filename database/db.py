import os.path
import sqlite3


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class BaseDbHelper:
    def __init__(self, path_to_db):
        self.path_to_db = path_to_db
        self._connect = sqlite3.connect(self.path_to_db)
        self.cursor = self._connect.cursor()

    def _execute_query(self, query):
        result = self.cursor.execute(query)
        self._connect.commit()
        return result


class DbHelper(BaseDbHelper):

    def get_all_tables(self):
        result = self._execute_query(f"SELECT name FROM sqlite_master WHERE type='table'")
        return result.fetchall()

    def create_table(self, table_name: str,
                     fields: str):
        result = self._execute_query(f"CREATE TABLE IF NOT EXISTS {table_name} "
                                     f"({fields})")
        return result

    def delete_table(self, table_name: str):
        self._execute_query(f"DROP TABLE IF EXISTS {table_name}")

    def get_rows_from_table(self, table: str,
                            filters='', field='*'):
        table = table
        filters = filters
        query = f'select {field} from {table}'
        if len(filters) > 0:
            query += f' where {filters}'
        result = self._execute_query(query).fetchall()
        return result if len(result) > 0 else [{}]

    def update_row(self, table: str,
                   key: str, value: str,
                   filters: str):
        query = f'update {table} set {key} = "{value}" where {filters}'
        self._execute_query(query)

    def insert_row(self, table: str,
                   columns: str, values: str):
        query = f"""INSERT INTO {table} ({columns}) values ({values})"""
        self._execute_query(query)

    def delete_row(self, table: str,
                   filters: str):
        query = f'delete from {table} where {filters}'
        self._execute_query(query)


@singleton
class DbMethods(DbHelper):

    def create_table_directories(self):
        self.create_table(table_name="directories",
                          fields="id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT")

    def create_table_files(self):
        self.create_table(table_name="files",
                          fields="id INTEGER PRIMARY KEY, directory_id INTEGER, "
                          "name TEXT, modified_date TEXT, permission INTEGER, "
                          "hash TEXT")

    def add_row_to_dir(self, parent_id, name):
        self.create_table_directories()
        self.insert_row(table="directories",
                        columns="parent_id, name",
                        values=f"{parent_id}, '{name}'")

    def add_row_to_file(self, directory_id, name, modified_date, permission, file_hash):
        self.create_table_files()
        self.insert_row(table="files",
                        columns="directory_id, name, modified_date, permission, hash",
                        values=f"{directory_id}, '{name}', '{modified_date}', {permission}, '{file_hash}'")

    def get_row(self, table, id_):
        row = self.get_rows_from_table(table=table,
                                       filters=f"id={id_}")
        return row


# db = DbMethods(os.path.abspath('db.sqlite3'))

# print(db is db1)
# print(db.get_all_tables())
# print(db.get_rows_from_table('directories'))

# db.delete_table("files")
# db.delete_table("directories")
# db.create_table_files()
# db.create_table_directories()
# # print(db.add_row_to_dir(3, "buy"))
# # db.add_row_to_file(2, "foo", "21.01.2022 15:65", 777, "HFDSAF635634DFSA")
# # print(db.get_rows_from_table('files'))
# print(db.get_rows_from_table('directories'))

