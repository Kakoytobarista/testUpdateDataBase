"""Runer for using script"""

import os

log_file = os.path.abspath("my_log.log")
source_root = os.path.abspath("testDir")
database_dir = os.path.abspath("database/db.sqlite3")


os.system(f"python3 fill_db.py --directory {source_root}  --database {database_dir}  --log {log_file} -v")
