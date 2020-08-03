import sqlite3

from pypika import Query
from pypika import Table
from pypika.pseudocolumns import RowID


class TeamRecordTable(object):
    def __init__(self) -> None:
        self.table = Table("teamrecord")

        self.value_table = TeamRecordValueTable()

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS teamrecord "
            + "(UUID TEXT NOT NULL UNIQUE, "
            + "SeasonID TEXT NOT NULL REFERENCES season(UUID), "
            + "Week INT, "
            + "UNIQUE(SeasonID, Week));",
        )

        self.value_table.create(cursor)

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Team Records:")
        cursor = connection.cursor()
        cursor.execute(Query.from_(self.table).select(RowID, self.table.star).get_sql())
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

        self.value_table.dump(connection)

    def drop(self, cursor: sqlite3.Cursor) -> None:
        self.value_table.drop(cursor)

        cursor.execute("DROP TABLE IF EXISTS teamrecord;")


class TeamRecordValueTable(object):
    def __init__(self) -> None:
        self.table = Table("teamrecordvalue")

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS teamrecordvalue "
            + "(TeamRecordID TEXT NOT NULL REFERENCES teamrecord(UUID), "
            + "TeamID TEXT NOT NULL REFERENCES team(UUID), "
            + "Wins INT NOT NULL, "
            + "Losses INT NOT NULL, "
            + "UNIQUE(TeamRecordID, TeamID));",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Team Record Values:")
        cursor = connection.cursor()
        cursor.execute(Query.from_(self.table).select(RowID, self.table.star).get_sql())
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute("DROP TABLE IF EXISTS teamrecordvalue;")
