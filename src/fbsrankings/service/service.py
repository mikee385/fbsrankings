from abc import ABCMeta
from types import TracebackType
from typing import ContextManager
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

from typing_extensions import Literal
from typing_extensions import Protocol

from fbsrankings.common import Command
from fbsrankings.common import CommandBus
from fbsrankings.common import EventBus
from fbsrankings.common import Query
from fbsrankings.common import QueryBus
from fbsrankings.domain import RaiseBehavior
from fbsrankings.domain import ValidationError
from fbsrankings.domain import ValidationService
from fbsrankings.infrastructure import QueryManagerFactory
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure.memory import DataSource as MemoryDataSource
from fbsrankings.infrastructure.sportsreference import SportsReference
from fbsrankings.infrastructure.sqlite import DataSource as SqliteDataSource
from fbsrankings.service.command import CommandManager
from fbsrankings.service.config import Config
from fbsrankings.service.config import ConfigStorageType

R = TypeVar("R", covariant=True)


class DataSource(QueryManagerFactory, TransactionFactory, Protocol, metaclass=ABCMeta):
    def drop(self) -> None:
        pass

    def close(self) -> None:
        pass

    def __enter__(self) -> "DataSource":
        pass

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        pass


class Service(ContextManager["Service"]):
    def __init__(self, config: Config, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._data_source: DataSource

        storage_type = config.storage_type
        if storage_type == ConfigStorageType.MEMORY:
            self._data_source = MemoryDataSource()

        elif storage_type == ConfigStorageType.SQLITE:
            database = config.database
            self._data_source = SqliteDataSource(str(database))

        else:
            raise ValueError(f"Unknown storage type: {storage_type}")

        alternate_names = config.alternate_names
        if alternate_names is None:
            alternate_names = {}

        self.validation_service = ValidationService(RaiseBehavior.ON_DEMAND)

        self._sports_reference = SportsReference(
            alternate_names,
            self.validation_service,
        )

        self._command_bus = CommandBus()
        self._command_manager = CommandManager(
            self._sports_reference,
            self._data_source,
            self._command_bus,
            self._event_bus,
        )

        self._query_bus = QueryBus()
        self._query_manager = self._data_source.query_manager(self._query_bus)

    @property
    def errors(self) -> List[ValidationError]:
        return self.validation_service.errors

    def send(self, command: Command) -> None:
        self._command_bus.send(command)

    def query(self, query: Query[R]) -> R:
        return self._query_bus.query(query)

    def drop(self) -> None:
        self._data_source.drop()

    def close(self) -> None:
        self._query_manager.close()
        self._command_manager.close()
        self._data_source.close()

    def __enter__(self) -> "Service":
        self._data_source.__enter__()
        self._command_manager.__enter__()
        self._query_manager.__enter__()
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self._query_manager.__exit__(type_, value, traceback)
        self._command_manager.__exit__(type_, value, traceback)
        self._data_source.__exit__(type_, value, traceback)
        return False
