from typing import Dict, Iterable, List, Optional, Tuple
from uuid import UUID


class AffiliationDto(object):
    def __init__(
        self, ID: UUID, season_ID: UUID, team_ID: UUID, subdivision: str
    ) -> None:
        self.ID = ID
        self.season_ID = season_ID
        self.team_ID = team_ID
        self.subdivision = subdivision


class AffiliationStorage(object):
    def __init__(self) -> None:
        self._by_ID: Dict[UUID, AffiliationDto] = {}
        self._by_key: Dict[Tuple[UUID, UUID], AffiliationDto] = {}
        self._by_season: Dict[UUID, List[AffiliationDto]] = {}

    def add(self, affiliation: AffiliationDto) -> None:
        key = (affiliation.season_ID, affiliation.team_ID)
        if key in self._by_key:
            raise ValueError(
                f"Affiliation already exists for team {affiliation.team_ID} in season {affiliation.season_ID}"
            )

        self._by_ID[affiliation.ID] = affiliation
        self._by_key[key] = affiliation

        by_season = self._by_season.get(affiliation.season_ID)
        if by_season is None:
            by_season = []
            self._by_season[affiliation.season_ID] = by_season
        by_season.append(affiliation)

    def get(self, ID: UUID) -> Optional[AffiliationDto]:
        return self._by_ID.get(ID)

    def find(self, season_ID: UUID, team_ID: UUID) -> Optional[AffiliationDto]:
        key = (season_ID, team_ID)
        return self._by_key.get(key)

    def by_season(self, season_ID: UUID) -> List[AffiliationDto]:
        by_season = self._by_season.get(season_ID)
        if by_season is None:
            return []
        return list(by_season)

    def all(self) -> Iterable[AffiliationDto]:
        return self._by_key.values()
