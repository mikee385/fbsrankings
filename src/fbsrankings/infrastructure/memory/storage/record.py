from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID

from dataclasses import dataclass


@dataclass(frozen=True)
class TeamRecordValueDto:
    team_id: UUID
    wins: int
    losses: int


@dataclass(frozen=True)
class TeamRecordDto:
    id_: UUID
    season_id: UUID
    week: Optional[int]
    values: List[TeamRecordValueDto]


class TeamRecordStorage:
    def __init__(self) -> None:
        self._by_id: Dict[UUID, TeamRecordDto] = {}
        self._by_key: Dict[Tuple[UUID, Optional[int]], TeamRecordDto] = {}
        self._by_season: Dict[UUID, List[TeamRecordDto]] = {}

    def add(self, record: TeamRecordDto) -> None:
        key = (record.season_id, record.week)

        existing = self._by_key.pop(key, None)
        if existing is not None:
            self._by_id.pop(existing.id_)
            self._by_season[existing.season_id].remove(existing)

        self._by_id[record.id_] = record
        self._by_key[key] = record

        by_season = self._by_season.get(record.season_id)
        if by_season is None:
            by_season = []
            self._by_season[record.season_id] = by_season
        by_season.append(record)

    def get(self, id_: UUID) -> Optional[TeamRecordDto]:
        return self._by_id.get(id_)

    def find(self, season_id: UUID, week: Optional[int]) -> Optional[TeamRecordDto]:
        key = (season_id, week)
        return self._by_key.get(key)

    def for_season(self, season_id: UUID) -> List[TeamRecordDto]:
        by_season = self._by_season.get(season_id)
        if by_season is None:
            return []
        return list(by_season)

    def all_(self) -> Iterable[TeamRecordDto]:
        return self._by_key.values()

    def drop(self) -> None:
        self._by_id = {}
        self._by_key = {}
        self._by_season = {}
