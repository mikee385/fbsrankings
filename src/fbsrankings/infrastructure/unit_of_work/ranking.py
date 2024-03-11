from typing import Iterable
from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import GameID
from fbsrankings.domain import GameRankingEventHandler as BaseGameEventHandler
from fbsrankings.domain import GameRankingRepository as BaseGameRepository
from fbsrankings.domain import Ranking
from fbsrankings.domain import RankingID
from fbsrankings.domain import RankingValue
from fbsrankings.domain import SeasonID
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRankingEventHandler as BaseTeamEventHandler
from fbsrankings.domain import TeamRankingRepository as BaseTeamRepository
from fbsrankings.event import GameRankingCalculatedEvent
from fbsrankings.event import TeamRankingCalculatedEvent
from fbsrankings.infrastructure.memory.write import (
    GameRankingRepository as MemoryGameRepository,
)
from fbsrankings.infrastructure.memory.write import (
    TeamRankingRepository as MemoryTeamRepository,
)


class TeamRankingRepository(BaseTeamRepository):
    def __init__(
        self,
        repository: BaseTeamRepository,
        cache: MemoryTeamRepository,
    ) -> None:
        super().__init__(repository._bus)
        self._cache = cache
        self._repository = repository

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


class TeamRankingEventHandler(BaseTeamEventHandler):
    def __init__(self, events: List[Event], bus: EventBus) -> None:
        super().__init__(bus)
        self._events = events

    def handle_calculated(self, event: TeamRankingCalculatedEvent) -> None:
        self._events.append(event)


class GameRankingRepository(BaseGameRepository):
    def __init__(
        self,
        repository: BaseGameRepository,
        cache: MemoryGameRepository,
    ) -> None:
        super().__init__(repository._bus)
        self._cache = cache
        self._repository = repository

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


class GameRankingEventHandler(BaseGameEventHandler):
    def __init__(self, events: List[Event], bus: EventBus) -> None:
        super().__init__(bus)
        self._events = events

    def handle_calculated(self, event: GameRankingCalculatedEvent) -> None:
        self._events.append(event)
