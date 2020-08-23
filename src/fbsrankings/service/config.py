from configparser import ConfigParser
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import AnyHttpUrl
from pydantic import BaseModel
from pydantic import PositiveInt
from typing_extensions import Literal


class ConfigStorageType(str, Enum):
    SQLITE = "sqlite"
    MEMORY = "memory"


class ConfigSourceType(str, Enum):
    URL = "URL"


class ConfigSeason(BaseModel):
    year: PositiveInt
    postseason_start_week: PositiveInt
    source_type: ConfigSourceType
    teams: Union[AnyHttpUrl, Path]
    games: Union[AnyHttpUrl, Path]


class Config(BaseModel):
    storage_type: ConfigStorageType
    database: Optional[Union[Path, Literal[":memory:"]]]
    alternate_names: Optional[Dict[str, str]]
    seasons: List[ConfigSeason]
    
    @staticmethod
    def from_ini(file_path: Path) -> "Config":
        data: Dict[str, Any] = {}

        parser = ConfigParser()
        parser.read(file_path)
    
        if "fbsrankings" not in parser:
            raise ValueError(f"{file_path}: No [fbsrankings] section in config file")
    
        for key, value in parser["fbsrankings"].items():
            data[key] = value
    
        seasons = []
        for header, section in parser.items():
            if header.startswith("fbsrankings."):
                name = header[12:]
                values = {key: value for key, value in section.items()}
    
                if name.startswith("season-"):
                    values["year"] = name[7:]
                    seasons.append(values)
                else:
                    data[name] = values
        data["seasons"] = seasons
    
        return Config(**data)
