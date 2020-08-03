import sqlite3

from pypika import Query
from pypika import Table
from pypika.pseudocolumns import RowID


class TeamTable(object):
    def __init__(self) -> None:
        self.table = Table("team")

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS team "
            + "(UUID TEXT NOT NULL UNIQUE, "
            + "Name TEXT NOT NULL UNIQUE);",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Teams:")
        cursor = connection.cursor()
        cursor.execute(Query.from_(self.table).select(RowID, self.table.star).get_sql())
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute("DROP TABLE IF EXISTS team;")
