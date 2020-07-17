from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID


class TeamRecordValueDto(object):
    def __init__(self, team_ID: UUID, wins: int, losses: int) -> None:
        self.team_ID = team_ID
        self.wins = wins
        self.losses = losses


class TeamRecordDto(object):
    def __init__(
        self,
        ID: UUID,
        season_ID: UUID,
        week: Optional[int],
        values: List[TeamRecordValueDto],
    ) -> None:
        self.ID = ID
        self.season_ID = season_ID
        self.week = week
        self.values = values


class TeamRecordStorage(object):
    def __init__(self) -> None:
        self._by_ID: Dict[UUID, TeamRecordDto] = {}
        self._by_key: Dict[Tuple[UUID, Optional[int]], TeamRecordDto] = {}
        self._by_season: Dict[UUID, List[TeamRecordDto]] = {}

    def add(self, record: TeamRecordDto) -> None:
        key = (record.season_ID, record.week)

        existing = self._by_key.pop(key, None)
        if existing is not None:
            self._by_ID.pop(existing.ID)
            self._by_season[existing.season_ID].remove(existing)

        self._by_ID[record.ID] = record
        self._by_key[key] = record

        by_season = self._by_season.get(record.season_ID)
        if by_season is None:
            by_season = []
            self._by_season[record.season_ID] = by_season
        by_season.append(record)

    def get(self, ID: UUID) -> Optional[TeamRecordDto]:
        return self._by_ID.get(ID)

    def find(self, season_ID: UUID, week: Optional[int],) -> Optional[TeamRecordDto]:
        key = (season_ID, week)
        return self._by_key.get(key)

    def for_season(self, season_ID: UUID) -> List[TeamRecordDto]:
        by_season = self._by_season.get(season_ID)
        if by_season is None:
            return []
        return list(by_season)

    def all(self) -> Iterable[TeamRecordDto]:
        return self._by_key.values()
