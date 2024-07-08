import sqlite3


class TeamTable:
    def __init__(self) -> None:
        self.table = "team"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(UUID TEXT NOT NULL UNIQUE, "
            "Name TEXT NOT NULL UNIQUE);",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Teams:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID,* FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")
