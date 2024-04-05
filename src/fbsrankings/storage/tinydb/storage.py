from pathlib import Path
from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from tinydb import TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
from typing_extensions import Literal


class Storage(ContextManager["Storage"]):
    def __init__(self, database: str) -> None:
        database_path = Path(database)
        if not database_path.is_absolute():
            sqlite_dir = Path(__file__).resolve().parent
            storage_dir = sqlite_dir.parent
            context_dir = storage_dir.parent
            package_dir = context_dir.parent
            database_path = package_dir / database

        database_path.parent.mkdir(parents=True, exist_ok=True)
        self._database = str(database_path)

        self.connection = TinyDB(
            self._database,
            storage=CachingMiddleware(JSONStorage),  # type: ignore
        )

    def drop(self) -> None:
        self.connection.drop_tables()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "Storage":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
