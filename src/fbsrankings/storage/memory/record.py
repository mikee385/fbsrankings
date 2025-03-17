from collections.abc import Iterable
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TeamRecordValueDto:
    team_id: str
    wins: int
    losses: int


@dataclass(frozen=True)
class TeamRecordDto:
    id_: str
    season_id: str
    week: Optional[int]
    values: list[TeamRecordValueDto]


class TeamRecordStorage:
    def __init__(self) -> None:
        self._by_id: dict[str, TeamRecordDto] = {}
        self._by_key: dict[tuple[str, Optional[int]], TeamRecordDto] = {}
        self._by_season: dict[str, list[TeamRecordDto]] = {}

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

    def get(self, id_: str) -> Optional[TeamRecordDto]:
        return self._by_id.get(id_)

    def find(self, season_id: str, week: Optional[int]) -> Optional[TeamRecordDto]:
        key = (season_id, week)
        return self._by_key.get(key)

    def for_season(self, season_id: str) -> list[TeamRecordDto]:
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
