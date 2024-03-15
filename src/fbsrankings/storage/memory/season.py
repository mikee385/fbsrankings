from typing import Dict
from typing import Iterable
from typing import Optional
from uuid import UUID

from dataclasses import dataclass


@dataclass(frozen=True)
class SeasonDto:
    id_: UUID
    year: int


class SeasonStorage:
    def __init__(self) -> None:
        self._by_id: Dict[UUID, SeasonDto] = {}
        self._by_key: Dict[int, SeasonDto] = {}

    def add(self, season: SeasonDto) -> None:
        if season.year in self._by_key:
            raise ValueError(f"Season already exists for year {season.year}")

        self._by_id[season.id_] = season
        self._by_key[season.year] = season

    def get(self, id_: UUID) -> Optional[SeasonDto]:
        return self._by_id.get(id_)

    def find(self, year: int) -> Optional[SeasonDto]:
        return self._by_key.get(year)

    def all_(self) -> Iterable[SeasonDto]:
        return self._by_key.values()

    def drop(self) -> None:
        self._by_id = {}
        self._by_key = {}
