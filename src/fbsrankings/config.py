from configparser import ConfigParser
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from pydantic import BaseModel
from typing_extensions import Literal


class ConfigCommandStorageType(str, Enum):
    MEMORY = "memory"
    SQLITE = "sqlite"


class ConfigQueryStorageType(str, Enum):
    MEMORY = "memory"
    SQLITE = "sqlite"
    TINYDB = "tinydb"


class Config(BaseModel):
    command_storage_type: ConfigCommandStorageType
    command_storage_file: Optional[Union[Path, Literal[":memory:"]]] = None

    query_storage_type: ConfigQueryStorageType
    query_storage_file: Optional[Union[Path, Literal[":memory:"]]] = None

    alternate_names: Optional[Dict[str, str]]

    @staticmethod
    def from_ini(file_path: Path) -> "Config":
        data: Dict[str, Any] = {}

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
