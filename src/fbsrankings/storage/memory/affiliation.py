from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from dataclasses import dataclass


@dataclass(frozen=True)
class AffiliationDto:
    id_: str
    season_id: str
    team_id: str
    subdivision: str


class AffiliationStorage:
    def __init__(self) -> None:
        self._by_id: Dict[str, AffiliationDto] = {}
        self._by_key: Dict[Tuple[str, str], AffiliationDto] = {}
        self._by_season: Dict[str, List[AffiliationDto]] = {}

    def add(self, affiliation: AffiliationDto) -> None:
        key = (affiliation.season_id, affiliation.team_id)
        if key in self._by_key:
            raise ValueError(
                f"Affiliation already exists for team {affiliation.team_id} in season"
                f" {affiliation.season_id}",
            )

        self._by_id[affiliation.id_] = affiliation
        self._by_key[key] = affiliation

        by_season = self._by_season.get(affiliation.season_id)
        if by_season is None:
            by_season = []
            self._by_season[affiliation.season_id] = by_season
        by_season.append(affiliation)

    def get(self, id_: str) -> Optional[AffiliationDto]:
        return self._by_id.get(id_)

    def find(self, season_id: str, team_id: str) -> Optional[AffiliationDto]:
        key = (season_id, team_id)
        return self._by_key.get(key)

    def for_season(self, season_id: str) -> List[AffiliationDto]:
        by_season = self._by_season.get(season_id)
        if by_season is None:
            return []
        return list(by_season)

    def all_(self) -> Iterable[AffiliationDto]:
        return self._by_key.values()

    def drop(self) -> None:
        self._by_id = {}
        self._by_key = {}
        self._by_season = {}
