from configparser import ConfigParser
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import PositiveInt
from typing_extensions import Literal


class ConfigStorageType(str, Enum):
    SQLITE = "sqlite"
    MEMORY = "memory"


class Config(BaseModel):
    storage_type: ConfigStorageType
    database: Optional[Union[Path, Literal[":memory:"]]]
    alternate_names: Optional[Dict[str, str]]
    seasons: List[PositiveInt]

    @staticmethod
    def from_ini(file_path: Path) -> "Config":
        data: Dict[str, Any] = {}

        parser = ConfigParser()
        parser.read(file_path)

        if "fbsrankings" not in parser:
            raise ValueError(f"{file_path}: No [fbsrankings] section in config file")

        for key, value in parser["fbsrankings"].items():
            if key == "seasons":
                data[key] = value.split()
            else:
                data[key] = value

        for header, section in parser.items():
            if header.startswith("fbsrankings."):
                name = header[12:]
                values = dict(section.items())
                data[name] = values

        return Config(**data)
