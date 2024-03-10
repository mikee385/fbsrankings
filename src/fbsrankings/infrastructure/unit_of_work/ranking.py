from typing import Iterable
from typing import Optional

from fbsrankings.domain import GameID
from fbsrankings.domain import GameRankingRepository as BaseGameRepository
from fbsrankings.domain import Ranking
from fbsrankings.domain import RankingID
from fbsrankings.domain import RankingValue
from fbsrankings.domain import SeasonID
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRankingRepository as BaseTeamRepository
from fbsrankings.event import GameRankingCalculatedEvent
from fbsrankings.event import TeamRankingCalculatedEvent
from fbsrankings.infrastructure.memory.storage import (
    RankingStorage as MemoryStorage,
)
from fbsrankings.infrastructure.memory.write import (
    GameRankingRepository as MemoryGameRepository,
)
from fbsrankings.infrastructure.memory.write import (
    TeamRankingRepository as MemoryTeamRepository,
)


class TeamRankingRepository(BaseTeamRepository):
    def __init__(self, repository: BaseTeamRepository) -> None:
        super().__init__(repository._bus)
        self._cache = MemoryTeamRepository(MemoryStorage(), self._bus)
        self._repository = repository

        self._bus.register_handler(
            TeamRankingCalculatedEvent,
            self._cache.handle_calculated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(
            TeamRankingCalculatedEvent,
            self._cache.handle_calculated,
        )

    def create(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
        values: Iterable[RankingValue[TeamID]],
    ) -> Ranking[TeamID]:
        return self._repository.create(name, season_id, week, values)

    def get(self, id_: RankingID) -> Optional[Ranking[TeamID]]:
        ranking = self._cache.get(id_)
        if ranking is None:
            ranking = self._repository.get(id_)
        return ranking

    def find(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
    ) -> Optional[Ranking[TeamID]]:
        ranking = self._cache.find(name, season_id, week)
        if ranking is None:
            ranking = self._repository.find(name, season_id, week)
        return ranking


class GameRankingRepository(BaseGameRepository):
    def __init__(self, repository: BaseGameRepository) -> None:
        super().__init__(repository._bus)
        self._cache = MemoryGameRepository(MemoryStorage(), self._bus)
        self._repository = repository

        self._bus.register_handler(
            GameRankingCalculatedEvent,
            self._cache.handle_calculated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(
            GameRankingCalculatedEvent,
            self._cache.handle_calculated,
        )

    def create(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
        values: Iterable[RankingValue[GameID]],
    ) -> Ranking[GameID]:
        return self._repository.create(name, season_id, week, values)

    def get(self, id_: RankingID) -> Optional[Ranking[GameID]]:
        ranking = self._cache.get(id_)
        if ranking is None:
            ranking = self._repository.get(id_)
        return ranking

    def find(
        self,
        name: str,
        season_id: SeasonID,
        week: Optional[int],
    ) -> Optional[Ranking[GameID]]:
        ranking = self._cache.find(name, season_id, week)
        if ranking is None:
            ranking = self._repository.find(name, season_id, week)
        return ranking
