import sqlite3

from fbsrankings.messages.enums import Subdivision


class SubdivisionTable:
    def __init__(self) -> None:
        self.table = "subdivision"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(Name TEXT NOT NULL UNIQUE, "
            "Number INT NOT NULL UNIQUE);",
        )

        cursor.execute(f"SELECT Number FROM {self.table};")
        existing = [row[0] for row in cursor.fetchall()]
        insert_sql = f"INSERT INTO {self.table} (Name, Number) VALUES (?, ?);"
        for value in Subdivision.DESCRIPTOR.values:
            if value.number not in existing:
                cursor.execute(
                    insert_sql,
                    [value.name, value.number],
                )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Subdivisions:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID, * FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")


class AffiliationTable:
    def __init__(self) -> None:
        self.table = "affiliation"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(UUID TEXT NOT NULL UNIQUE, "
            "SeasonID TEXT NOT NULL REFERENCES season(UUID), "
            "TeamID TEXT NOT NULL REFERENCES team(UUID), "
            "Subdivision INT NOT NULL REFERENCES subdivision(Number), "
            "UNIQUE(SeasonID, TeamID));",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Affiliations:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID,* FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")
