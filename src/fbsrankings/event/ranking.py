from abc import ABCMeta
from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.common import Event


class RankingValue:
    def __init__(self, id_: UUID, order: int, rank: int, value: float) -> None:
        self.id_ = id_
        self.order = order
        self.rank = rank
        self.value = value


class RankingCalculatedEvent(Event, metaclass=ABCMeta):
    def __init__(
        self,
        id_: UUID,
        name: str,
        season_id: UUID,
        week: Optional[int],
        values: List[RankingValue],
    ) -> None:
        self.id_ = id_
        self.name = name
        self.season_id = season_id
        self.week = week
        self.values = values


class TeamRankingCalculatedEvent(RankingCalculatedEvent):
    pass


class GameRankingCalculatedEvent(RankingCalculatedEvent):
    pass