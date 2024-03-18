import sqlite3
from pathlib import Path
from types import TracebackType
from typing import Any
from typing import ContextManager
from typing import Optional
from typing import Type

from cachetools import TTLCache
from typing_extensions import Literal

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
    def __init__(self, database: str) -> None:
        self.cache = TTLCache[str, Any](  # pylint: disable=unsubscriptable-object
            maxsize=16384,
            ttl=60,
        )

        if database == ":memory:":
            self._database = database
        else:
            database_path = Path(database)
            if not database_path.is_absolute():
                sqlite_dir = Path(__file__).resolve().parent
                storage_dir = sqlite_dir.parent
                context_dir = storage_dir.parent
                package_dir = context_dir.parent
                database_path = package_dir / database

            database_path.parent.mkdir(parents=True, exist_ok=True)
            self._database = str(database_path)

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
