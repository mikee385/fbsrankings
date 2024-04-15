"""Memory storage classes for the fbsrankings package"""
from .affiliation import AffiliationDto
from .affiliation import AffiliationStorage
from .game import GameDto
from .game import GameStorage
from .ranking import RankingDto
from .ranking import RankingStorage
from .ranking import RankingValueDto
from .record import TeamRecordDto
from .record import TeamRecordStorage
from .record import TeamRecordValueDto
from .season import SeasonDto
from .season import SeasonStorage
from .storage import Storage
from .team import TeamDto
from .team import TeamStorage


__all__ = [
    "AffiliationDto",
    "AffiliationStorage",
    "GameDto",
    "GameStorage",
    "RankingDto",
    "RankingStorage",
    "RankingValueDto",
    "SeasonDto",
    "SeasonStorage",
    "Storage",
    "TeamDto",
    "TeamRecordDto",
    "TeamRecordStorage",
    "TeamRecordValueDto",
    "TeamStorage",
]
