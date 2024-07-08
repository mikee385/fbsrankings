import sqlite3


class TeamRecordTable:
    def __init__(self) -> None:
        self.table = "teamrecord"

        self.value_table = TeamRecordValueTable()

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(UUID TEXT NOT NULL UNIQUE, "
            "SeasonID TEXT NOT NULL REFERENCES season(UUID), "
            "Week INT, "
            "UNIQUE(SeasonID, Week));",
        )

        self.value_table.create(cursor)

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Team Records:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID,* FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

        self.value_table.dump(connection)

    def drop(self, cursor: sqlite3.Cursor) -> None:
        self.value_table.drop(cursor)

        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")


class TeamRecordValueTable:
    def __init__(self) -> None:
        self.table = "teamrecordvalue"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table} "
            "(TeamRecordID TEXT NOT NULL REFERENCES teamrecord(UUID), "
            "TeamID TEXT NOT NULL REFERENCES team(UUID), "
            "Wins INT NOT NULL, "
            "Losses INT NOT NULL, "
            "UNIQUE(TeamRecordID, TeamID));",
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Team Record Values:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ROWID,* FROM {self.table};")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.table};")
