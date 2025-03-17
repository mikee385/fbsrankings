from types import TracebackType
from typing import ContextManager
from typing import Literal
from typing import Optional
from typing import Union

from fbsrankings.config import Config
from fbsrankings.config import StorageType
from fbsrankings.storage.memory.storage import Storage as MemoryStorage
from fbsrankings.storage.sqlite.storage import Storage as SqliteStorage
from fbsrankings.storage.tinydb.storage import Storage as TinyDbStorage


class Context(ContextManager["Context"]):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.command_storage: Union[MemoryStorage, SqliteStorage]
        self.query_storage: Union[MemoryStorage, SqliteStorage, TinyDbStorage]

        if config.storage == StorageType.MEMORY_SHARED:
            self.command_storage = MemoryStorage()
            self.query_storage = self.command_storage

        elif config.storage == StorageType.SQLITE_SHARED:
            self.command_storage = SqliteStorage(config.sqlite.file)
            self.query_storage = self.command_storage

        elif config.storage == StorageType.SQLITE_TINYDB:
            self.command_storage = SqliteStorage(config.sqlite.file)
            self.query_storage = TinyDbStorage(config.tinydb.file)

        else:
            raise ValueError(f"Unknown storage type: {config.storage}")

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
        type_: Optional[type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.query_storage.__exit__(type_, value, traceback)
        self.command_storage.__exit__(type_, value, traceback)
        return False
