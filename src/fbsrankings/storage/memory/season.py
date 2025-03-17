from collections.abc import Iterable
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SeasonDto:
    id_: str
    year: int


class SeasonStorage:
    def __init__(self) -> None:
        self._by_id: dict[str, SeasonDto] = {}
        self._by_key: dict[int, SeasonDto] = {}

    def add(self, season: SeasonDto) -> None:
        if season.year in self._by_key:
            raise ValueError(f"Season already exists for year {season.year}")

        self._by_id[season.id_] = season
        self._by_key[season.year] = season

    def get(self, id_: str) -> Optional[SeasonDto]:
        return self._by_id.get(id_)

    def find(self, year: int) -> Optional[SeasonDto]:
        return self._by_key.get(year)

    def all_(self) -> Iterable[SeasonDto]:
        return self._by_key.values()

    def drop(self) -> None:
        self._by_id = {}
        self._by_key = {}
