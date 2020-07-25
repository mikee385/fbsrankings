import sqlite3

from fbsrankings.infrastructure.sqlite.storage.affiliation import AffiliationTable
from fbsrankings.infrastructure.sqlite.storage.affiliation import SubdivisionTable
from fbsrankings.infrastructure.sqlite.storage.game import GameStatusTable
from fbsrankings.infrastructure.sqlite.storage.game import GameTable
from fbsrankings.infrastructure.sqlite.storage.ranking import RankingTable
from fbsrankings.infrastructure.sqlite.storage.ranking import RankingTypeTable
from fbsrankings.infrastructure.sqlite.storage.record import TeamRecordTable
from fbsrankings.infrastructure.sqlite.storage.season import SeasonSectionTable
from fbsrankings.infrastructure.sqlite.storage.season import SeasonTable
from fbsrankings.infrastructure.sqlite.storage.team import TeamTable


class Storage(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
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

            TeamRecordTable().create(cursor)
            RankingTable().create(cursor)

            cursor.execute("commit")
        except:  # noqa: E722
            cursor.execute("rollback")
            raise
        finally:
            cursor.close()

    def drop(self, connection: sqlite3.Connection) -> None:
        cursor = connection.cursor()
        cursor.execute("begin")
        try:
            RankingTable().drop(cursor)
            TeamRecordTable().drop(cursor)

            GameTable().drop(cursor)
            AffiliationTable().drop(cursor)
            TeamTable().drop(cursor)
            SeasonTable().drop(cursor)

            RankingTypeTable().drop(cursor)
            GameStatusTable().drop(cursor)
            SubdivisionTable().drop(cursor)
            SeasonSectionTable().drop(cursor)

            SeasonSectionTable().create(cursor)
            SubdivisionTable().create(cursor)
            GameStatusTable().create(cursor)
            RankingTypeTable().create(cursor)

            SeasonTable().create(cursor)
            TeamTable().create(cursor)
            AffiliationTable().create(cursor)
            GameTable().create(cursor)

            TeamRecordTable().create(cursor)
            RankingTable().create(cursor)

            cursor.execute("commit")
        except:  # noqa: E722
            cursor.execute("rollback")
            raise
        finally:
            cursor.close()
