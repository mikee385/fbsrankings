import sqlite3

from fbsrankings.messages.enums import GameStatus
from fbsrankings.messages.enums import SeasonSection


class SeasonSectionTable:
    def __init__(self) -> None:
        self.table = "seasonsection"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(Name TEXT NOT NULL UNIQUE, "
            "Number INT NOT NULL UNIQUE);",
        )

        cursor.execute(f"SELECT Number FROM {self.table};")
        existing = [row[0] for row in cursor.fetchall()]
        insert_sql = f"INSERT INTO {self.table} (Name, Number) VALUES (?, ?);"
        for value in SeasonSection.DESCRIPTOR.values:
            if value.number not in existing:
                cursor.execute(
                    insert_sql,
                    [value.name, value.number],
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


class GameStatusTable:
    def __init__(self) -> None:
        self.table = "gamestatus"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(Name TEXT NOT NULL UNIQUE, "
            "Number INT NOT NULL UNIQUE);",
        )

        cursor.execute(f"SELECT Number FROM {self.table};")
        existing = [row[0] for row in cursor.fetchall()]
        insert_sql = f"INSERT INTO {self.table} (Name, Number) VALUES (?, ?);"
        for value in GameStatus.DESCRIPTOR.values:
            if value.number not in existing:
                cursor.execute(
                    insert_sql,
                    [value.name, value.number],
                )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Game Statuses:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID, * FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")


class GameTable:
    def __init__(self) -> None:
        self.table = "game"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(UUID TEXT NOT NULL UNIQUE, "
            "SeasonID TEXT NOT NULL REFERENCES season(UUID), "
            "Week INT NOT NULL, "
            "Date DATE NOT NULL, "
            "SeasonSection INT NOT NULL REFERENCES seasonsection(Number), "
            "HomeTeamID TEXT NOT NULL REFERENCES team(UUID), "
            "AwayTeamID TEXT NOT NULL REFERENCES team(UUID), "
            "HomeTeamScore INT NULL, "
            "AwayTeamScore INT NULL, "
            "Status INT NOT NULL REFERENCES gamestatus(Number), "
            "Notes TEXT NOT NULL, UNIQUE(SeasonID, Week, HomeTeamID, AwayTeamID));",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Games:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID,* FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")
