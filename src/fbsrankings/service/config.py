from typing import Dict
from typing import List

from typing_extensions import TypedDict


class ConfigSettings(TypedDict):
    storage_type: str


class ConfigSettingsSqlite(ConfigSettings, total=False):
    database: str


class ConfigSeason(TypedDict):
    year: int
    postseason_start_week: int
    source_type: str
    teams: str
    games: str


class Config(TypedDict):
    settings: ConfigSettingsSqlite
    alternate_names: Dict[str, str]
    seasons: List[ConfigSeason]