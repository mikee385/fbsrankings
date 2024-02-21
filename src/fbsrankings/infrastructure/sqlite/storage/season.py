import sqlite3

from pypika import Parameter
from pypika import Query
from pypika import Table
from pypika.pseudocolumns import RowID

from fbsrankings.domain import SeasonSection


class SeasonSectionTable:
    def __init__(self) -> None:
        self.table = Table("seasonsection")

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS seasonsection (Name TEXT NOT NULL UNIQUE);",
        )

        cursor.execute(Query.from_(self.table).select(self.table.Name).get_sql())
        existing = [row[0] for row in cursor.fetchall()]
        insert_sql = (
            Query.into(self.table)
            .columns(self.table.Name)
            .insert(Parameter("?"))
            .get_sql()
        )
        for value in SeasonSection:
            if value.name not in existing:
                cursor.execute(
                    insert_sql,
                    [value.name],
                )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Season Sections:")
        cursor = connection.cursor()
        cursor.execute(Query.from_(self.table).select(RowID, self.table.star).get_sql())
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    @staticmethod
    def drop(cursor: sqlite3.Cursor) -> None:
        cursor.execute("DROP TABLE IF EXISTS seasonsection;")


class SeasonTable:
    def __init__(self) -> None:
        self.table = Table("season")

    @staticmethod
    def create(cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS season "
            + "(UUID TEXT NOT NULL UNIQUE, "
            + "Year INT  NOT NULL UNIQUE);",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Seasons:")
        cursor = connection.cursor()
        cursor.execute(Query.from_(self.table).select(RowID, self.table.star).get_sql())
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    @staticmethod
    def drop(cursor: sqlite3.Cursor) -> None:
        cursor.execute("DROP TABLE IF EXISTS season;")
