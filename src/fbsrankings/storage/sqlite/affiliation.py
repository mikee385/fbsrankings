import sqlite3

from fbsrankings.shared.enums import Subdivision


class SubdivisionTable:
    def __init__(self) -> None:
        self.table = "subdivision"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} (Name TEXT NOT NULL UNIQUE);",
        )

        cursor.execute(f"SELECT Name FROM {self.table};")
        existing = [row[0] for row in cursor.fetchall()]
        insert_sql = f"INSERT INTO {self.table} (Name) VALUES (?);"
        for value in Subdivision:
            if value.name not in existing:
                cursor.execute(
                    insert_sql,
                    [value.name],
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
            "Subdivision TEXT NOT NULL REFERENCES subdivision(Name), "
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
