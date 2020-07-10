from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.common import Event


class RankingValue(object):
    def __init__(self, ID: UUID, order: int, rank: int, value: float) -> None:
        self.ID = ID
        self.order = order
        self.rank = rank
        self.value = value


class RankingCalculatedEvent(Event):
    def __init__(
        self,
        ID: UUID,
        name: str,
        season_ID: UUID,
        week: Optional[int],
        values: List[RankingValue],
    ) -> None:
        self.ID = ID
        self.name = name
        self.season_ID = season_ID
        self.week = week
        self.values = values

