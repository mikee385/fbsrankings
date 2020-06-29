import os
import sqlite3

from fbsrankings.infrastructure.sqlite.storage.affiliation import AffiliationTable
from fbsrankings.infrastructure.sqlite.storage.affiliation import SubdivisionTable
from fbsrankings.infrastructure.sqlite.storage.game import GameStatusTable
from fbsrankings.infrastructure.sqlite.storage.game import GameTable
from fbsrankings.infrastructure.sqlite.storage.season import SeasonSectionTable
from fbsrankings.infrastructure.sqlite.storage.season import SeasonTable
from fbsrankings.infrastructure.sqlite.storage.team import TeamTable


class Storage(object):
    def __init__(self, database: str) -> None:
        self.database = database

        directory = os.path.dirname(self.database)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

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

                SeasonTable().create(cursor)
                TeamTable().create(cursor)
                AffiliationTable().create(cursor)
                GameTable().create(cursor)

                cursor.execute("commit")
            except:  # noqa: E722
                cursor.execute("rollback")
                raise
            finally:
                cursor.close()
        finally:
            connection.close()
