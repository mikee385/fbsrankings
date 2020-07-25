import sqlite3


class TeamRecordTable(object):
    def __init__(self) -> None:
        self.name = "teamrecord"
        self.columns = "UUID, SeasonID, Week"

        self.value_table = TeamRecordValueTable()

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.name}
            (UUID TEXT NOT NULL UNIQUE,
             SeasonID TEXT NOT NULL REFERENCES season(UUID),
             Week INT,
             UNIQUE(SeasonID, Week));"""
        )

        self.value_table.create(cursor)

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Team Records:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT rowid, * FROM {self.name}")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

        self.value_table.dump(connection)

    def drop(self, cursor: sqlite3.Cursor) -> None:
        self.value_table.drop(cursor)

        cursor.execute(f"DROP TABLE IF EXISTS {self.name}")


class TeamRecordValueTable(object):
    def __init__(self) -> None:
        self.name = "teamrecordvalue"
        self.columns = "TeamRecordID, TeamID, Wins, Losses"

    def create(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.name}
            (TeamRecordID TEXT NOT NULL REFERENCES teamrecord(UUID),
             TeamID TEXT NOT NULL REFERENCES team(UUID),
             Wins INT NOT NULL,
             Losses INT NOT NULL,
             UNIQUE(TeamRecordID, TeamID));"""
        )

    def dump(self, connection: sqlite3.Connection) -> None:
        print("Team Record Values:")
        cursor = connection.cursor()
        cursor.execute(f"SELECT rowid, * FROM {self.name}")
        for row in cursor.fetchall():
            print("(" + ", ".join(str(item) for item in row) + ")")
        cursor.close()

    def drop(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(f"DROP TABLE IF EXISTS {self.name}")
