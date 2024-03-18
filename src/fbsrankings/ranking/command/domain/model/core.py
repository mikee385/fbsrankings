from enum import Enum
from typing import NewType
from uuid import UUID


class SeasonSection(Enum):
    REGULAR_SEASON = 1
    POSTSEASON = 2


SeasonID = NewType("SeasonID", UUID)


TeamID = NewType("TeamID", UUID)


class Subdivision(Enum):
    FBS = 1
    FCS = 2


class GameStatus(Enum):
    SCHEDULED = 0
    COMPLETED = 1
    CANCELED = 2


GameID = NewType("GameID", UUID)
