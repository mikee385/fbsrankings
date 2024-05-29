from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type
from typing import Union

from typing_extensions import Literal

from fbsrankings.shared.config import Config
from fbsrankings.shared.config import ConfigCommandStorageType
from fbsrankings.shared.config import ConfigQueryStorageType
from fbsrankings.storage.memory.storage import Storage as MemoryStorage
from fbsrankings.storage.sqlite.storage import Storage as SqliteStorage
from fbsrankings.storage.tinydb.storage import Storage as TinyDbStorage


class Context(ContextManager["Context"]):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.command_storage: Union[MemoryStorage, SqliteStorage]
        self.query_storage: Union[MemoryStorage, SqliteStorage, TinyDbStorage]

        if config.command_storage_type == ConfigCommandStorageType.MEMORY:
            self.command_storage = MemoryStorage()

        elif config.command_storage_type == ConfigCommandStorageType.SQLITE:
            self.command_storage = SqliteStorage(config.command_storage_file)

        else:
            raise ValueError(
                f"Unknown command storage type: {config.command_storage_type}",
            )

        if config.query_storage_type.name == config.command_storage_type.name:
            self.query_storage = self.command_storage

        elif config.query_storage_type == ConfigQueryStorageType.TINYDB:
            self.query_storage = TinyDbStorage(config.query_storage_file)

        else:
            raise ValueError(
                "Query storage type must either be equal to command storage type "
                f"or 'tinydb': {config.query_storage_type}",
            )

    def drop_storage(self) -> None:
        self.command_storage.drop()
        self.query_storage.drop()

    def close(self) -> None:
        self.query_storage.close()
        self.command_storage.close()

    def __enter__(self) -> "Context":
        self.command_storage.__enter__()
        self.query_storage.__enter__()
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.query_storage.__exit__(type_, value, traceback)
        self.command_storage.__exit__(type_, value, traceback)
        return False
