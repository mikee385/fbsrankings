import sqlite3
from pathlib import Path
from types import TracebackType
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.common import QueryBus
from fbsrankings.infrastructure import QueryManagerFactory
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure.sqlite.read import QueryManager
from fbsrankings.infrastructure.sqlite.storage import Storage
from fbsrankings.infrastructure.sqlite.write import Transaction


class DataSource(QueryManagerFactory, TransactionFactory):
    def __init__(self, database: str) -> None:
        if database == ":memory:":
            self._database = database
        else:
            database_path = Path(database)
            if not database_path.is_absolute():
                sqlite_dir = Path(__file__).resolve().parent
                infrastructure_dir = sqlite_dir.parent
                package_dir = infrastructure_dir.parent
                database_path = package_dir / database

            database_path.parent.mkdir(parents=True, exist_ok=True)
            self._database = str(database_path)

        self._connection = sqlite3.connect(self._database, isolation_level=None)
        self._connection.execute("PRAGMA foreign_keys = ON")

        self._storage = Storage(self._connection)

    def query_manager(self, query_bus: QueryBus) -> QueryManager:
        return QueryManager(self._connection, query_bus)

    def transaction(self, event_bus: EventBus) -> Transaction:
        return Transaction(self._connection, event_bus)

    def drop(self) -> None:
        self._storage.drop(self._connection)

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> "DataSource":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
