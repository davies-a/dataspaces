import datetime
import os
import sqlite3
import time

from dspace.config import ConfigStore


def adapt_datetime(ts):
    return time.mktime(ts.timetuple())


sqlite3.register_adapter(datetime.datetime, adapt_datetime)


class SnapshotController:
    _config: ConfigStore
    db_conn: sqlite3.Connection

    def __init__(self, config: ConfigStore) -> None:
        self._config = config or ConfigStore.get_or_create()
        self.snapshots_directory = os.path.join(
            self._config._config_folder, "snapshots"
        )
        self.snapshots_file_path = os.path.join(
            self.snapshots_directory, "directory.db"
        )
        self.db_conn = sqlite3.connect(self.snapshots_file_path)
        self.bootstrap_db()

    def get_snapshot_directory(self, name: str):
        path_elements = [self._config._config_folder, "snapshots"]
        if name:
            path_elements.append(name)

        snapshot_directory = os.path.join(*path_elements)

        if not os.path.exists(snapshot_directory):
            os.makedirs(snapshot_directory, exist_ok=True)

        return snapshot_directory

    def bootstrap_db(self):
        cur = self.db_conn.cursor()
        cur.execute(
            "create table if not exists snapshots "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name VARCHAR(200),"
            "created_at DEFAULT CURRENT_TIMESTAMP"
            ")"
        )
        cur.close()

    def add_snapshot(self, name: str):
        cursor = self.db_conn.cursor()
        cursor.execute(f"INSERT INTO snapshots(name) VALUES (?)", (name,))
        self.db_conn.commit()
        cursor.close()

    def get_snapshots(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM snapshots")
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_snapshot(self, name: str):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM snapshots WHERE name=?", (name,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def delete_snapshot(self, name: str):
        cursor = self.db_conn.cursor()
        cursor.execute(f"DELETE FROM snapshots where name=?", (name,))
        self.db_conn.commit()
        cursor.close()

    def delete_all_snapshots(self, name: str):
        cursor = self.db_conn.cursor()
        cursor.execute(f"DELETE FROM snapshots")
        self.db_conn.commit()
        cursor.close()
