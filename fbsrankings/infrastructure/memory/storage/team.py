from typing import Dict, Iterable, Optional
from uuid import UUID


class TeamDto(object):
    def __init__(self, ID: UUID, name: str) -> None:
        self.ID = ID
        self.name = name


class TeamStorage(object):
    def __init__(self) -> None:
        self._by_ID: Dict[UUID, TeamDto] = {}
        self._by_key: Dict[str, TeamDto] = {}

    def add(self, team: TeamDto) -> None:
        if team.name in self._by_key:
            raise ValueError(f"Team already exists for name {team.name}")

        self._by_ID[team.ID] = team
        self._by_key[team.name] = team

    def get(self, ID: UUID) -> Optional[TeamDto]:
        return self._by_ID.get(ID)

    def find(self, name: str) -> Optional[TeamDto]:
        return self._by_key.get(name)

    def all(self) -> Iterable[TeamDto]:
        return self._by_key.values()
