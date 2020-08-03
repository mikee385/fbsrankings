import sqlite3
from enum import Enum

from pypika import Parameter
from pypika import Query
from pypika import Table
from pypika.pseudocolumns import RowID


class RankingType(Enum):
    TEAM = 0
    GAME = 1


class RankingTypeTable(object):
    def __init__(self) -> None:
        self.table = Table("rankingtype")

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS rankingtype
        (Name TEXT NOT NULL UNIQUE);"""
        )

        cursor.execute(
            Query.from_(self.table)
            .select(self.table.Name)
            .get_sql()
        )
        existing = [row[0] for row in cursor.fetchall()]
        for value in RankingType:
            if value.name not in existing:
                cursor.execute(
                    Query.into(self.table)
                    .columns(self.table.Name)
                    .insert(Parameter("?"))
                    .get_sql(),
                    [value.name],
                )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Ranking Types:")
        cursor = connection.cursor()
        cursor.execute(
            Query.from_(self.table)
            .select(RowID, self.table.star)
            .get_sql()
        )
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute("DROP TABLE IF EXISTS rankingtype")


class RankingTable(object):
    def __init__(self) -> None:
        self.table = Table("ranking")
        self.columns = "UUID, Name, Type, SeasonID, Week"

        self.team_value_table = TeamRankingValueTable()
        self.game_value_table = GameRankingValueTable()

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS ranking
            (UUID TEXT NOT NULL UNIQUE,
             Name TEXT NOT NULL,
             Type TEXT NOT NULL REFERENCES rankingtype(Name),
             SeasonID TEXT NOT NULL REFERENCES season(UUID),
             Week INT,
             UNIQUE(Name, SeasonID, Week));"""
        )

        self.team_value_table.create(cursor)
        self.game_value_table.create(cursor)

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Rankings:")
        cursor = connection.cursor()
        cursor.execute(
            Query.from_(self.table)
            .select(RowID, self.table.star)
            .get_sql()
        )
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

        self.team_value_table.dump(connection)
        self.game_value_table.dump(connection)

    def drop(self, cursor: sqlite3.Cursor) -> None:
        self.game_value_table.drop(cursor)
        self.team_value_table.drop(cursor)

        cursor.execute(f"DROP TABLE IF EXISTS ranking")


class TeamRankingValueTable(object):
    def __init__(self) -> None:
        self.table = Table("teamrankingvalue")
        self.columns = "RankingID, TeamID, Ord, Rank, Value"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS teamrankingvalue
            (RankingID TEXT NOT NULL REFERENCES ranking(UUID),
             TeamID TEXT NOT NULL REFERENCES team(UUID),
             Ord INT NOT NULL,
             Rank INT NOT NULL,
             Value REAL NOT NULL,
             UNIQUE(RankingID, TeamID),
             UNIQUE(RankingID, Ord));"""
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Team Ranking Values:")
        cursor = connection.cursor()
        cursor.execute(
            Query.from_(self.table)
            .select(RowID, self.table.star)
            .get_sql()
        )
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS teamrankingvalue")


class GameRankingValueTable(object):
    def __init__(self) -> None:
        self.table = Table("gamerankingvalue")
        self.columns = "RankingID, GameID, Ord, Rank, Value"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS gamerankingvalue
            (RankingID TEXT NOT NULL REFERENCES ranking(UUID),
             GameID TEXT NOT NULL REFERENCES game(UUID),
             Ord INT NOT NULL,
             Rank INT NOT NULL,
             Value REAL NOT NULL,
             UNIQUE(RankingID, GameID),
             UNIQUE(RankingID, Ord));"""
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Game Ranking Values:")
        cursor = connection.cursor()
        cursor.execute(
            Query.from_(self.table)
            .select(RowID, self.table.star)
            .get_sql()
        )
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute("DROP TABLE IF EXISTS gamerankingvalue")
