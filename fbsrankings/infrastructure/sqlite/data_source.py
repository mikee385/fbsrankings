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
        elif Path(database).is_absolute():
            self._database = database
        else:
            sqlite_dir = Path(__file__).resolve().parent
            infrastructure_dir = sqlite_dir.parent
            package_dir = infrastructure_dir.parent
            self._database = str(package_dir / database)

        self._storage = Storage(self._database)

    def query_manager(self, query_bus: QueryBus) -> QueryManager:
        return QueryManager(self._database, query_bus)

    def transaction(self, event_bus: EventBus) -> Transaction:
        return Transaction(self._database, event_bus)

    def close(self) -> None:
        pass

    def __enter__(self) -> "DataSource":
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
