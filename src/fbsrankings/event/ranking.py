from abc import ABCMeta
from typing import List
from typing import Optional
from uuid import UUID

from dataclasses import dataclass

from fbsrankings.common import Event


@dataclass(frozen=True)
class RankingValue:
    id_: UUID
    order: int
    rank: int
    value: float


@dataclass(frozen=True)
class RankingCalculatedEvent(Event, metaclass=ABCMeta):
    id_: UUID
    name: str
    season_id: UUID
    week: Optional[int]
    values: List[RankingValue]


@dataclass(frozen=True)
class TeamRankingCalculatedEvent(RankingCalculatedEvent):
    pass


@dataclass(frozen=True)
class GameRankingCalculatedEvent(RankingCalculatedEvent):
    pass
