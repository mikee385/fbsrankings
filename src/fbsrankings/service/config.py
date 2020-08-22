from enum import Enum
from pathlib import Path
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
