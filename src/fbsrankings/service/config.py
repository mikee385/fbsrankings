from typing import Dict
from typing import List

from typing_extensions import TypedDict


class ConfigSeason(TypedDict):
    year: int
    postseason_start_week: int
    source_type: str
    teams: str
    games: str


class BaseConfig(TypedDict):
    storage_type: str
    alternate_names: Dict[str, str]
    seasons: List[ConfigSeason]


class Config(BaseConfig, total=False):
    database: str
