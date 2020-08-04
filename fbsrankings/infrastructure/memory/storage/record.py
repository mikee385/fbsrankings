from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID


class TeamRecordValueDto(object):
    def __init__(self, team_id: UUID, wins: int, losses: int) -> None:
        self.team_id = team_id
        self.wins = wins
        self.losses = losses


class TeamRecordDto(object):
    def __init__(
        self,
        id: UUID,
        season_id: UUID,
        week: Optional[int],
        values: List[TeamRecordValueDto],
    ) -> None:
        self.id = id
        self.season_id = season_id
        self.week = week
        self.values = values


class TeamRecordStorage(object):
    def __init__(self) -> None:
        self._by_id: Dict[UUID, TeamRecordDto] = {}
        self._by_key: Dict[Tuple[UUID, Optional[int]], TeamRecordDto] = {}
        self._by_season: Dict[UUID, List[TeamRecordDto]] = {}

    def add(self, record: TeamRecordDto) -> None:
        key = (record.season_id, record.week)

        existing = self._by_key.pop(key, None)
        if existing is not None:
            self._by_id.pop(existing.id)
            self._by_season[existing.season_id].remove(existing)

        self._by_id[record.id] = record
        self._by_key[key] = record

        by_season = self._by_season.get(record.season_id)
        if by_season is None:
            by_season = []
            self._by_season[record.season_id] = by_season
        by_season.append(record)

    def get(self, id: UUID) -> Optional[TeamRecordDto]:
        return self._by_id.get(id)

    def find(self, season_id: UUID, week: Optional[int]) -> Optional[TeamRecordDto]:
        key = (season_id, week)
        return self._by_key.get(key)

    def for_season(self, season_id: UUID) -> List[TeamRecordDto]:
        by_season = self._by_season.get(season_id)
        if by_season is None:
            return []
        return list(by_season)

    def all(self) -> Iterable[TeamRecordDto]:
        return self._by_key.values()

    def drop(self) -> None:
        self._by_id = {}
        self._by_key = {}
        self._by_season = {}
