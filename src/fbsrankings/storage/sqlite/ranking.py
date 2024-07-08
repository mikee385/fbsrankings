import sqlite3
from enum import Enum


class RankingType(Enum):
    TEAM = 0
    GAME = 1


class RankingTypeTable:
    def __init__(self) -> None:
        self.table = "rankingtype"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(Name TEXT NOT NULL UNIQUE);",
        )

        cursor.execute(f"SELECT Name FROM {self.table};")
        existing = [row[0] for row in cursor.fetchall()]
        insert_sql = f"INSERT INTO {self.table} (Name) VALUES (?);"
        for value in RankingType:
            if value.name not in existing:
                cursor.execute(
                    insert_sql,
                    [value.name],
                )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Ranking Types:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID, * FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")


class RankingTable:
    def __init__(self) -> None:
        self.table = "ranking"

        self.team_value_table = TeamRankingValueTable()
        self.game_value_table = GameRankingValueTable()

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(UUID TEXT NOT NULL UNIQUE, "
            "Name TEXT NOT NULL, "
            "Type TEXT NOT NULL REFERENCES rankingtype(Name), "
            "SeasonID TEXT NOT NULL REFERENCES season(UUID), "
            "Week INT, "
            "UNIQUE(Name, SeasonID, Week));",
        )

        self.team_value_table.create(cursor)
        self.game_value_table.create(cursor)

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Rankings:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID,* FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

        self.team_value_table.dump(connection)
        self.game_value_table.dump(connection)

    def drop(self, cursor: sqlite3.Cursor) -> None:
        self.game_value_table.drop(cursor)
        self.team_value_table.drop(cursor)

        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")


class TeamRankingValueTable:
    def __init__(self) -> None:
        self.table = "teamrankingvalue"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(RankingID TEXT NOT NULL REFERENCES ranking(UUID), "
            "TeamID TEXT NOT NULL REFERENCES team(UUID), "
            "Ord INT NOT NULL, "
            "Rank INT NOT NULL, "
            "Value REAL NOT NULL, "
            "UNIQUE(RankingID, TeamID), "
            "UNIQUE(RankingID, Ord));",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Team Ranking Values:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID,* FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")


class GameRankingValueTable:
    def __init__(self) -> None:
        self.table = "gamerankingvalue"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(RankingID TEXT NOT NULL REFERENCES ranking(UUID), "
            "GameID TEXT NOT NULL REFERENCES game(UUID), "
            "Ord INT NOT NULL, "
            "Rank INT NOT NULL, "
            "Value REAL NOT NULL, "
            "UNIQUE(RankingID, GameID), "
            "UNIQUE(RankingID, Ord));",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Game Ranking Values:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID,* FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")
