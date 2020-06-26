from typing import Dict
from typing import Iterable
from typing import Optional
from uuid import UUID


class SeasonDto(object):
    def __init__(self, ID: UUID, year: int) -> None:
        self.ID = ID
        self.year = year


class SeasonStorage(object):
    def __init__(self) -> None:
        self._by_ID: Dict[UUID, SeasonDto] = {}
        self._by_key: Dict[int, SeasonDto] = {}

    def add(self, season: SeasonDto) -> None:
        if season.year in self._by_key:
            raise ValueError(f"Season already exists for year {season.year}")

        self._by_ID[season.ID] = season
        self._by_key[season.year] = season

    def get(self, ID: UUID) -> Optional[SeasonDto]:
        return self._by_ID.get(ID)

    def find(self, year: int) -> Optional[SeasonDto]:
        return self._by_key.get(year)

    def all(self) -> Iterable[SeasonDto]:
        return self._by_key.values()
