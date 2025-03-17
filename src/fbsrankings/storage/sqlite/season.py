import sqlite3


class SeasonTable:
    def __init__(self) -> None:
        self.table = "season"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(UUID TEXT NOT NULL UNIQUE, "
            "Year INT NOT NULL UNIQUE);",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Seasons:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID,* FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")
