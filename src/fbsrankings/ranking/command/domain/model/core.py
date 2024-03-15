from enum import Enum

from fbsrankings.common import Identifier


class SeasonSection(Enum):
    REGULAR_SEASON = 1
    POSTSEASON = 2


class SeasonID(Identifier):
    pass


class TeamID(Identifier):
    pass


class Subdivision(Enum):
    FBS = 1
    FCS = 2


class GameStatus(Enum):
    SCHEDULED = 0
    COMPLETED = 1
    CANCELED = 2


class GameID(Identifier):
    pass
