from typing import Union

from communication.bus import EventBus
from fbsrankings.config import ConfigCommandStorageType
from fbsrankings.context import Context
from fbsrankings.core.command.infrastructure.event_handler import EventHandler
from fbsrankings.core.command.infrastructure.event_handler import EventHandlerFactory
from fbsrankings.core.command.infrastructure.memory.data_source import (
    DataSource as MemoryDataSource,
)
from fbsrankings.core.command.infrastructure.repository import Repository
from fbsrankings.core.command.infrastructure.repository import RepositoryFactory
from fbsrankings.core.command.infrastructure.sqlite.data_source import (
    DataSource as SqliteDataSource,
)
from fbsrankings.storage.memory import Storage as MemoryStorage
from fbsrankings.storage.sqlite import Storage as SqliteStorage


class DataSource(RepositoryFactory, EventHandlerFactory):
    def __init__(self, context: Context) -> None:
        self._data_source: Union[MemoryDataSource, SqliteDataSource]

        storage_type = context.config.command_storage_type
        if storage_type == ConfigCommandStorageType.MEMORY:
            if not isinstance(context.command_storage, MemoryStorage):
                raise ValueError(
                    f"For command storage type, expected: MemoryStorage, "
                    f"found: {type(context.command_storage)}",
                )
            self._data_source = MemoryDataSource(context.command_storage)

        elif storage_type == ConfigCommandStorageType.SQLITE:
            if not isinstance(context.command_storage, SqliteStorage):
                raise ValueError(
                    f"For command storage type, expected: SqliteStorage, "
                    f"found: {type(context.command_storage)}",
                )
            self._data_source = SqliteDataSource(context.command_storage)

        else:
            raise ValueError(f"Unknown command storage type: {storage_type}")

    def repository(self, event_bus: EventBus) -> Repository:
        return self._data_source.repository(event_bus)

    def event_handler(self, event_bus: EventBus) -> EventHandler:
        return self._data_source.event_handler(event_bus)
