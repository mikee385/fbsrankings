from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type
from typing import Union

from typing_extensions import Literal

from communication.bus import EventBus
from communication.bus import QueryBus
from fbsrankings.config import ConfigQueryStorageType
from fbsrankings.context import Context
from fbsrankings.ranking.query.infrastructure.memory.query_manager import (
    QueryManager as MemoryQueryManager,
)
from fbsrankings.ranking.query.infrastructure.sqlite.query_manager import (
    QueryManager as SqliteQueryManager,
)
from fbsrankings.ranking.query.infrastructure.tinydb.query_manager import (
    QueryManager as TinyDbQueryManager,
)
from fbsrankings.storage.memory import Storage as MemoryStorage
from fbsrankings.storage.sqlite import Storage as SqliteStorage
from fbsrankings.storage.tinydb import Storage as TinyDbStorage


class Service(ContextManager["Service"]):
    def __init__(
        self,
        context: Context,
        query_bus: QueryBus,
        event_bus: EventBus,
    ) -> None:
        self._query_manager: Union[
            MemoryQueryManager,
            SqliteQueryManager,
            TinyDbQueryManager,
        ]

        storage_type = context.config.query_storage_type
        if storage_type == ConfigQueryStorageType.MEMORY:
            if not isinstance(context.query_storage, MemoryStorage):
                raise ValueError(
                    "For query storage type, expected: MemoryStorage, "
                    f"found: {type(context.query_storage)}",
                )
            self._query_manager = MemoryQueryManager(context.query_storage, query_bus)

        elif storage_type == ConfigQueryStorageType.SQLITE:
            if not isinstance(context.query_storage, SqliteStorage):
                raise ValueError(
                    "For query storage type, expected: SqliteStorage, "
                    f"found: {type(context.query_storage)}",
                )
            self._query_manager = SqliteQueryManager(context.query_storage, query_bus)

        elif storage_type == ConfigQueryStorageType.TINYDB:
            if not isinstance(context.query_storage, TinyDbStorage):
                raise ValueError(
                    "For query storage type, expected: TinyDbStorage, "
                    f"found: {type(context.query_storage)}",
                )
            self._query_manager = TinyDbQueryManager(
                context.query_storage,
                query_bus,
                event_bus,
            )

        else:
            raise ValueError(f"Unknown query storage type: {storage_type}")

    def close(self) -> None:
        self._query_manager.close()

    def __enter__(self) -> "Service":
        self._query_manager.__enter__()
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self._query_manager.__exit__(type_, value, traceback)
        return False
