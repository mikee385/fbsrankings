from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type
from typing import Union

from typing_extensions import Literal

from fbsrankings.common import QueryBus as BaseQueryBus
from fbsrankings.config import ConfigStorageType
from fbsrankings.context import Context
from fbsrankings.core.query.infrastructure.memory.query_manager import (
    QueryManager as MemoryQueryManager,
)
from fbsrankings.core.query.infrastructure.sqlite.query_manager import (
    QueryManager as SqliteQueryManager,
)
from fbsrankings.storage.memory import Storage as MemoryStorage
from fbsrankings.storage.sqlite import Storage as SqliteStorage


class QueryBus(BaseQueryBus, ContextManager["QueryBus"]):
    def __init__(self, context: Context) -> None:
        super().__init__()
        self._query_manager: Union[MemoryQueryManager, SqliteQueryManager]

        storage_type = context.config.storage_type
        if storage_type == ConfigStorageType.MEMORY:
            if not isinstance(context.storage, MemoryStorage):
                raise ValueError(
                    f"For storage type, expected: {MemoryStorage}, "
                    f"found: {type(context.storage)}",
                )
            self._query_manager = MemoryQueryManager(context.storage, self)

        elif storage_type == ConfigStorageType.SQLITE:
            if not isinstance(context.storage, SqliteStorage):
                raise ValueError(
                    f"For storage type, expected: {SqliteStorage}, "
                    f"found: {type(context.storage)}",
                )
            self._query_manager = SqliteQueryManager(context.storage, self)

        else:
            raise ValueError(f"Unknown storage type: {storage_type}")

    def close(self) -> None:
        self._query_manager.close()

    def __enter__(self) -> "QueryBus":
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
