from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID

from dataclasses import dataclass


@dataclass(frozen=True)
class RankingValueDto:
    id_: UUID
    order: int
    rank: int
    value: float


@dataclass(frozen=True)
class RankingDto:
    id_: UUID
    name: str
    season_id: UUID
    week: Optional[int]
    values: List[RankingValueDto]


class RankingStorage:
    def __init__(self) -> None:
        self._by_id: Dict[UUID, RankingDto] = {}
        self._by_key: Dict[Tuple[str, UUID, Optional[int]], RankingDto] = {}
        self._by_season: Dict[UUID, List[RankingDto]] = {}

    def add(self, ranking: RankingDto) -> None:
        key = (ranking.name, ranking.season_id, ranking.week)

        existing = self._by_key.pop(key, None)
        if existing is not None:
            self._by_id.pop(existing.id_)
            self._by_season[existing.season_id].remove(existing)

        self._by_id[ranking.id_] = ranking
        self._by_key[key] = ranking

        by_season = self._by_season.get(ranking.season_id)
        if by_season is None:
            by_season = []
            self._by_season[ranking.season_id] = by_season
        by_season.append(ranking)

    def get(self, id_: UUID) -> Optional[RankingDto]:
        return self._by_id.get(id_)

    def find(
        self,
        name: str,
        season_id: UUID,
        week: Optional[int],
    ) -> Optional[RankingDto]:
        key = (name, season_id, week)
        return self._by_key.get(key)

    def for_season(self, season_id: UUID) -> List[RankingDto]:
        by_season = self._by_season.get(season_id)
        if by_season is None:
            return []
        return list(by_season)

    def all_(self) -> Iterable[RankingDto]:
        return self._by_key.values()

    def drop(self) -> None:
        self._by_id = {}
        self._by_key = {}
        self._by_season = {}
