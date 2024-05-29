from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.ranking.command.domain.model.factory import Factory
from fbsrankings.ranking.command.infrastructure.data_source import DataSource
from fbsrankings.ranking.command.infrastructure.memory.event_handler import (
    EventHandler as MemoryEventHandler,
)
from fbsrankings.ranking.command.infrastructure.memory.repository import (
    Repository as MemoryRepository,
)
from fbsrankings.ranking.command.infrastructure.repository import Repository
from fbsrankings.ranking.command.infrastructure.transaction.event_handler import (
    EventHandler as TransactionEventHandler,
)
from fbsrankings.ranking.command.infrastructure.transaction.repository import (
    Repository as TransactionRepository,
)
from fbsrankings.shared.messaging import EventBus
from fbsrankings.storage.memory import Storage as MemoryStorage


class Transaction(ContextManager["Transaction"]):
    def __init__(self, data_source: DataSource, bus: EventBus) -> None:
        self._data_source = data_source
        self._outer_bus = bus
        self._inner_bus = EventBus()

        self._factory = Factory(self._inner_bus)
        self._data_repository = self._data_source.repository(self._inner_bus)

        self._cache_bus = EventBus()
        self._cache_storage = MemoryStorage()
        self._cache_repository = MemoryRepository(self._cache_storage, self._inner_bus)
        self._cache_handler = MemoryEventHandler(self._cache_storage, self._cache_bus)

        self._repository = TransactionRepository(
            self._data_repository,
            self._cache_repository,
            self._cache_bus,
        )
        self._event_handler = TransactionEventHandler(self._inner_bus, self._cache_bus)

    @property
    def factory(self) -> Factory:
        return self._factory

    @property
    def repository(self) -> Repository:
        return self._repository

    def commit(self) -> None:
        storage_bus = EventBus()
        with self._data_source.event_handler(storage_bus) as event_handler:
            for event in self._event_handler.events:
                storage_bus.publish(event)
            event_handler.close()

        for event in self._event_handler.events:
            self._outer_bus.publish(event)

        self._cache_storage.drop()
        self._event_handler.clear()

    def rollback(self) -> None:
        self._cache_storage.drop()
        self._event_handler.clear()

    def close(self) -> None:
        self._event_handler.close()
        self._event_handler.clear()
        self._cache_handler.close()
        self._cache_storage.drop()
        self._cache_storage.close()

    def __enter__(self) -> "Transaction":
        self._cache_storage.__enter__()
        self._cache_handler.__enter__()
        self._event_handler.__enter__()
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        self._event_handler.__exit__(type_, value, traceback)
        self._cache_handler.__exit__(type_, value, traceback)
        self._cache_storage.__exit__(type_, value, traceback)
        return False
