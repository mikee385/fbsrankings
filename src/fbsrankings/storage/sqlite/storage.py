import sqlite3
from pathlib import Path
from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.config import SqliteFile
from fbsrankings.storage.sqlite.affiliation import AffiliationTable
from fbsrankings.storage.sqlite.affiliation import SubdivisionTable
from fbsrankings.storage.sqlite.game import GameStatusTable
from fbsrankings.storage.sqlite.game import GameTable
from fbsrankings.storage.sqlite.ranking import RankingTable
from fbsrankings.storage.sqlite.ranking import RankingTypeTable
from fbsrankings.storage.sqlite.record import TeamRecordTable
from fbsrankings.storage.sqlite.season import SeasonSectionTable
from fbsrankings.storage.sqlite.season import SeasonTable
from fbsrankings.storage.sqlite.team import TeamTable


class Storage(ContextManager["Storage"]):
    def __init__(self, storage_file: SqliteFile) -> None:
        if isinstance(storage_file, Path):
            storage_file.parent.mkdir(parents=True, exist_ok=True)
            self._database = str(storage_file)

        elif storage_file == ":memory:":
            self._database = storage_file

        else:
            raise TypeError("SQLite storage file must be a Path or ':memory:'")

        self.connection = sqlite3.connect(self._database, isolation_level=None)
        self.connection.execute("PRAGMA foreign_keys = ON")

        cursor = self.connection.cursor()
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
        except Exception:
            cursor.execute("rollback")
            raise
        finally:
            cursor.close()

    def drop(self) -> None:
        cursor = self.connection.cursor()
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
        except Exception:
            cursor.execute("rollback")
            raise
        finally:
            cursor.close()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "Storage":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
