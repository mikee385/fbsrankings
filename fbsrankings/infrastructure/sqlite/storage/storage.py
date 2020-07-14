import sqlite3
from pathlib import Path

from fbsrankings.infrastructure.sqlite.storage.affiliation import AffiliationTable
from fbsrankings.infrastructure.sqlite.storage.affiliation import SubdivisionTable
from fbsrankings.infrastructure.sqlite.storage.game import GameStatusTable
from fbsrankings.infrastructure.sqlite.storage.game import GameTable
from fbsrankings.infrastructure.sqlite.storage.ranking import RankingTable
from fbsrankings.infrastructure.sqlite.storage.ranking import RankingTypeTable
from fbsrankings.infrastructure.sqlite.storage.season import SeasonSectionTable
from fbsrankings.infrastructure.sqlite.storage.season import SeasonTable
from fbsrankings.infrastructure.sqlite.storage.team import TeamTable


class Storage(object):
    def __init__(self, database: str) -> None:
        self.database = database

        Path(self.database).resolve().parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(database)
        try:
            connection.isolation_level = None
            connection.execute("PRAGMA foreign_keys = ON")

            cursor = connection.cursor()
            cursor.execute("begin")
            try:
                SeasonSectionTable().create(cursor)
                SubdivisionTable().create(cursor)
                GameStatusTable().create(cursor)
                RankingTypeTable().create(cursor)

                SeasonTable().create(cursor)
                TeamTable().create(cursor)
                AffiliationTable().create(cursor)
                GameTable().create(cursor)
                RankingTable().create(cursor)

                cursor.execute("commit")
            except:  # noqa: E722
                cursor.execute("rollback")
                raise
            finally:
                cursor.close()
        finally:
            connection.close()
