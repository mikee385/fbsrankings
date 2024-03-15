from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type
from typing import Union

from typing_extensions import Literal

from fbsrankings.config import Config
from fbsrankings.config import ConfigStorageType
from fbsrankings.storage.memory.storage import Storage as MemoryStorage
from fbsrankings.storage.sqlite.storage import Storage as SqliteStorage


class Context(ContextManager["Context"]):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.storage: Union[MemoryStorage, SqliteStorage]

        storage_type = config.storage_type
        if storage_type == ConfigStorageType.MEMORY:
            self.storage = MemoryStorage()

        elif storage_type == ConfigStorageType.SQLITE:
            database = config.database
            self.storage = SqliteStorage(str(database))

        else:
            raise ValueError(f"Unknown storage type: {storage_type}")

    def close(self) -> None:
        self.storage.close()

    def __enter__(self) -> "Context":
        self.storage.__enter__()
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.storage.__exit__(type_, value, traceback)
        return False
