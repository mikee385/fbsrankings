from typing import Dict
from typing import Iterable
from typing import Optional
from uuid import UUID


class TeamDto:
    def __init__(self, id_: UUID, name: str) -> None:
        self.id_ = id_
        self.name = name


class TeamStorage:
    def __init__(self) -> None:
        self._by_id: Dict[UUID, TeamDto] = {}
        self._by_key: Dict[str, TeamDto] = {}

    def add(self, team: TeamDto) -> None:
        if team.name in self._by_key:
            raise ValueError(f"Team already exists for name {team.name}")

        self._by_id[team.id_] = team
        self._by_key[team.name] = team

    def get(self, id_: UUID) -> Optional[TeamDto]:
        return self._by_id.get(id_)

    def find(self, name: str) -> Optional[TeamDto]:
        return self._by_key.get(name)

    def all(self) -> Iterable[TeamDto]:
        return self._by_key.values()

    def drop(self) -> None:
        self._by_id = {}
        self._by_key = {}