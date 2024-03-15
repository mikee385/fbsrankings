import sqlite3

from pypika import Parameter
from pypika import Query
from pypika import Table
from pypika.pseudocolumns import RowID

from fbsrankings.enum import Subdivision


class SubdivisionTable:
    def __init__(self) -> None:
        self.table = Table("subdivision")

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS subdivision (Name TEXT NOT NULL UNIQUE);",
        )

        cursor.execute(Query.from_(self.table).select(self.table.Name).get_sql())
        existing = [row[0] for row in cursor.fetchall()]
        insert_sql = (
            Query.into(self.table)
            .columns(self.table.Name)
            .insert(Parameter("?"))
            .get_sql()
        )
        for value in Subdivision:
            if value.name not in existing:
                cursor.execute(
                    insert_sql,
                    [value.name],
                )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Subdivisions:")
        cursor = connection.cursor()
        cursor.execute(Query.from_(self.table).select(RowID, self.table.star).get_sql())
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    @staticmethod
    def drop(cursor: sqlite3.Cursor) -> None:
        cursor.execute("DROP TABLE IF EXISTS subdivision;")


class AffiliationTable:
    def __init__(self) -> None:
        self.table = Table("affiliation")

    @staticmethod
    def create(cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS affiliation "
            "(UUID TEXT NOT NULL UNIQUE, "
            "SeasonID TEXT NOT NULL REFERENCES season(UUID), "
            "TeamID TEXT NOT NULL REFERENCES team(UUID), "
            "Subdivision TEXT NOT NULL REFERENCES subdivision(Name), "
            "UNIQUE(SeasonID, TeamID));",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Affiliations:")
        cursor = connection.cursor()
        cursor.execute(Query.from_(self.table).select(RowID, self.table.star).get_sql())
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    @staticmethod
    def drop(cursor: sqlite3.Cursor) -> None:
        cursor.execute("DROP TABLE IF EXISTS affiliation;")
