from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID


class RankingValueDto(object):
    def __init__(self, ID: UUID, order: int, rank: int, value: float) -> None:
        self.ID = ID
        self.order = order
        self.rank = rank
        self.value = value


class RankingDto(object):
    def __init__(
        self,
        ID: UUID,
        name: str,
        season_ID: UUID,
        week: Optional[int],
        values: List[RankingValueDto],
    ) -> None:
        self.ID = ID
        self.name = name
        self.season_ID = season_ID
        self.week = week
        self.values = values


class RankingStorage(object):
    def __init__(self) -> None:
        self._by_ID: Dict[UUID, RankingDto] = {}
        self._by_key: Dict[Tuple[str, UUID, Optional[int]], RankingDto] = {}
        self._by_season: Dict[UUID, List[RankingDto]] = {}

    def add(self, ranking: RankingDto) -> None:
        key = (ranking.name, ranking.season_ID, ranking.week)

        existing = self._by_key.pop(key, None)
        if existing is not None:
            self._by_ID.pop(existing.ID)
            self._by_season[existing.season_ID].remove(existing)

        self._by_ID[ranking.ID] = ranking
        self._by_key[key] = ranking

        by_season = self._by_season.get(ranking.season_ID)
        if by_season is None:
            by_season = []
            self._by_season[ranking.season_ID] = by_season
        by_season.append(ranking)

    def get(self, ID: UUID) -> Optional[RankingDto]:
        return self._by_ID.get(ID)

    def find(
        self, name: str, season_ID: UUID, week: Optional[int],
    ) -> Optional[RankingDto]:
        key = (name, season_ID, week)
        return self._by_key.get(key)

    def for_season(self, season_ID: UUID) -> List[RankingDto]:
        by_season = self._by_season.get(season_ID)
        if by_season is None:
            return []
        return list(by_season)

    def all(self) -> Iterable[RankingDto]:
        return self._by_key.values()

    def drop(self) -> None:
        self._by_ID = {}
        self._by_key = {}
        self._by_season = {}
