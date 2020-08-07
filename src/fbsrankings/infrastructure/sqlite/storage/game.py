import sqlite3

from pypika import Parameter
from pypika import Query
from pypika import Table
from pypika.pseudocolumns import RowID

from fbsrankings.domain import GameStatus


class GameStatusTable:
    def __init__(self) -> None:
        self.table = Table("gamestatus")

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS gamestatus (Name TEXT NOT NULL UNIQUE);",
        )

        cursor.execute(Query.from_(self.table).select(self.table.Name).get_sql())
        existing = [row[0] for row in cursor.fetchall()]
        insert_sql = (
            Query.into(self.table)
            .columns(self.table.Name)
            .insert(Parameter("?"))
            .get_sql()
        )
        for value in GameStatus:
            if value.name not in existing:
                cursor.execute(
                    insert_sql, [value.name],
                )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Game Statuses:")
        cursor = connection.cursor()
        cursor.execute(Query.from_(self.table).select(RowID, self.table.star).get_sql())
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    @staticmethod
    def drop(cursor: sqlite3.Cursor) -> None:
        cursor.execute("DROP TABLE IF EXISTS gamestatus;")


class GameTable:
    def __init__(self) -> None:
        self.table = Table("game")

    @staticmethod
    def create(cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS game "
            + "(UUID TEXT NOT NULL UNIQUE, "
            + "SeasonID TEXT NOT NULL REFERENCES season(UUID), "
            + "Week INT NOT NULL, "
            + "Date DATE NOT NULL, "
            + "SeasonSection TEXT NOT NULL REFERENCES seasonsection(Name), "
            + "HomeTeamID TEXT NOT NULL REFERENCES team(UUID), "
            + "AwayTeamID TEXT NOT NULL REFERENCES team(UUID), "
            + "HomeTeamScore INT NULL, "
            + "AwayTeamScore INT NULL, "
            + "Status TEXT NOT NULL REFERENCES gamestatus(Name), "
            + "Notes TEXT NOT NULL, UNIQUE(SeasonID, Week, HomeTeamID, AwayTeamID));",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Games:")
        cursor = connection.cursor()
        cursor.execute(Query.from_(self.table).select(RowID, self.table.star).get_sql())
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    @staticmethod
    def drop(cursor: sqlite3.Cursor) -> None:
        cursor.execute("DROP TABLE IF EXISTS game;")
