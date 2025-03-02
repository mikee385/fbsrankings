import sqlite3

from fbsrankings.messages.enums import GameStatus


class GameStatusTable:
    def __init__(self) -> None:
        self.table = "gamestatus"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} (Name TEXT NOT NULL UNIQUE);",
        )

        cursor.execute(f"SELECT Name FROM {self.table};")
        existing = [row[0] for row in cursor.fetchall()]
        insert_sql = f"INSERT INTO {self.table} (Name) VALUES (?);"
        for value in GameStatus:
            if value.name not in existing:
                cursor.execute(
                    insert_sql,
                    [value.name],
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
            "SeasonSection TEXT NOT NULL REFERENCES seasonsection(Name), "
            "HomeTeamID TEXT NOT NULL REFERENCES team(UUID), "
            "AwayTeamID TEXT NOT NULL REFERENCES team(UUID), "
            "HomeTeamScore INT NULL, "
            "AwayTeamScore INT NULL, "
            "Status TEXT NOT NULL REFERENCES gamestatus(Name), "
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
