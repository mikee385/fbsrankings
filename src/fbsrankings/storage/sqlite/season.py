import sqlite3

from fbsrankings.messages.enums import SeasonSection


class SeasonSectionTable:
    def __init__(self) -> None:
        self.table = "seasonsection"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} (Name TEXT NOT NULL UNIQUE);",
        )

        cursor.execute(f"SELECT Name FROM {self.table};")
        existing = [row[0] for row in cursor.fetchall()]
        insert_sql = f"INSERT INTO {self.table} (Name) VALUES (?);"
        for value in SeasonSection:
            if value.name not in existing:
                cursor.execute(
                    insert_sql,
                    [value.name],
                )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Season Sections:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID, * FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")


class SeasonTable:
    def __init__(self) -> None:
        self.table = "season"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(UUID TEXT NOT NULL UNIQUE, "
            "Year INT  NOT NULL UNIQUE);",
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
