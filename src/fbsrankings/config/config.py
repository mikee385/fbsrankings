from configparser import ConfigParser
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Literal
from typing import Union

from pydantic import BaseModel


class ChannelType(str, Enum):
    NONE = "none"
    MEMORY = "memory"


class SerializationType(str, Enum):
    NONE = "none"
    JSON = "json"
    PICKLE = "pickle"
    PROTOBUF = "protobuf"


class StorageType(str, Enum):
    MEMORY_SHARED = "memory-shared"
    SQLITE_SHARED = "sqlite-shared"
    SQLITE_TINYDB = "sqlite-tinydb"


SqliteFile = Union[Path, Literal[":memory:"]]


class SqliteConfig(BaseModel):
    file: SqliteFile


TinyDbFile = Path


class TinyDbConfig(BaseModel):
    file: TinyDbFile


class Config(BaseModel):
    channel: ChannelType
    serialization: SerializationType
    storage: StorageType

    alternate_names: dict[str, str] = {}

    sqlite: SqliteConfig = SqliteConfig(file="fbsrankings.db")
    tinydb: TinyDbConfig = TinyDbConfig(file="fbsrankings.json")

    @staticmethod
    def from_ini(file_path: Path) -> "Config":
        data: dict[str, Any] = {}

        parser = ConfigParser()
        parser.read(file_path)

        if "fbsrankings" not in parser:
            raise ValueError(f"{file_path}: No [fbsrankings] section in config file")

        for key, value in parser["fbsrankings"].items():
            data[key] = value

        for header, section in parser.items():
            if header.startswith("fbsrankings."):
                name = header[12:]
                values = dict(section.items())
                data[name] = values

        return Config(**data)
