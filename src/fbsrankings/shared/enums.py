from enum import Enum


class SeasonSection(Enum):
    REGULAR_SEASON = 1
    POSTSEASON = 2


class Subdivision(Enum):
    FBS = 1
    FCS = 2


class GameStatus(Enum):
    SCHEDULED = 0
    COMPLETED = 1
    CANCELED = 2
