from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.common import QueryBus
from fbsrankings.infrastructure import DataSource as BaseDataSource
from fbsrankings.infrastructure.memory.read import QueryManager
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.infrastructure.memory.write import EventHandler
from fbsrankings.infrastructure.memory.write import Repository


class DataSource(BaseDataSource, ContextManager["DataSource"]):
    def __init__(self) -> None:
        super().__init__()
        self._storage = Storage()

    def repository(self, event_bus: EventBus) -> Repository:
        return Repository(self._storage, event_bus)

    def event_handler(self, event_bus: EventBus) -> EventHandler:
        return EventHandler(self._storage, event_bus)

    def query_manager(self, query_bus: QueryBus) -> QueryManager:
        return QueryManager(self._storage, query_bus)

    def drop(self) -> None:
        self._storage.drop()

    def close(self) -> None:
        pass

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
