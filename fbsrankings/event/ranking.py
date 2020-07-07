from typing import List
from typing import Optional
from uuid import UUID

from fbsrankings.common import Event


class RankingValue(object):
    def __init__(self, ID: UUID, rank: int, order: int, value: float) -> None:
        self.ID = ID
        self.rank = rank
        self.order = order
        self.value = value


class RankingCreatedEvent(Event):
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


class RankingValuesUpdatedEvent(Event):
    def __init__(self, ID: UUID, values: List[RankingValue]) -> None:
        self.ID = ID
        self.values = values
