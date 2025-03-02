from pathlib import Path
from types import TracebackType
from typing import ContextManager
from typing import Dict
from typing import Optional
from typing import Type

from tinydb import TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
from tinydb.table import Document
from typing_extensions import Literal

from fbsrankings.config import ConfigStorageFile


class Storage(ContextManager["Storage"]):
    def __init__(self, storage_file: ConfigStorageFile) -> None:
        if storage_file is None:
            storage_file = Path("fbsrankings.json")
            storage_file.parent.mkdir(parents=True, exist_ok=True)
            self._database = str(storage_file)

        elif isinstance(storage_file, Path):
            storage_file.parent.mkdir(parents=True, exist_ok=True)
            self._database = str(storage_file)

        else:
            raise TypeError("TinyDB storage file must be a Path or None")

        self.connection = TinyDB(
            self._database,
            storage=CachingMiddleware(JSONStorage),  # type: ignore
        )

        self.cache_season_by_id: Dict[str, Document] = {}
        self.cache_season_by_year: Dict[int, Document] = {}
        for item in self.connection.table("seasons").all():
            self.cache_season_by_id[item["id_"]] = item
            self.cache_season_by_year[item["year"]] = item

        self.cache_team_by_id: Dict[str, Document] = {}
        self.cache_team_by_name: Dict[str, Document] = {}
        for item in self.connection.table("teams").all():
            self.cache_team_by_id[item["id_"]] = item
            self.cache_team_by_name[item["name"]] = item

        self.cache_game_by_id: Dict[str, Document] = {}
        for item in self.connection.table("games").all():
            self.cache_game_by_id[item["id_"]] = item

    def drop(self) -> None:
        self.connection.drop_tables()

        self.cache_season_by_id = {}
        self.cache_season_by_year = {}
        self.cache_team_by_id = {}
        self.cache_team_by_name = {}
        self.cache_game_by_id = {}

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
