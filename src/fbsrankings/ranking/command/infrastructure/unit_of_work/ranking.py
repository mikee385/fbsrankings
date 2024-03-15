from typing import Iterable
from typing import List
from typing import Optional

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.ranking.command.domain.model.core import GameID
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.domain.model.ranking import (
    GameRankingEventHandler as BaseGameEventHandler,
)
from fbsrankings.ranking.command.domain.model.ranking import (
    GameRankingRepository as BaseGameRepository,
)
from fbsrankings.ranking.command.domain.model.ranking import Ranking
from fbsrankings.ranking.command.domain.model.ranking import RankingID
from fbsrankings.ranking.command.domain.model.ranking import RankingValue
from fbsrankings.ranking.command.domain.model.ranking import (
    TeamRankingEventHandler as BaseTeamEventHandler,
)
from fbsrankings.ranking.command.domain.model.ranking import (
    TeamRankingRepository as BaseTeamRepository,
)
from fbsrankings.ranking.command.event.ranking import GameRankingCalculatedEvent
from fbsrankings.ranking.command.event.ranking import RankingValue as EventValue
from fbsrankings.ranking.command.event.ranking import TeamRankingCalculatedEvent
from fbsrankings.ranking.command.infrastructure.memory.ranking import (
    GameRankingRepository as MemoryGameRepository,
)
from fbsrankings.ranking.command.infrastructure.memory.ranking import (
    TeamRankingRepository as MemoryTeamRepository,
)


class TeamRankingRepository(BaseTeamRepository):
    def __init__(
        self,
        repository: BaseTeamRepository,
        cache: MemoryTeamRepository,
        cache_bus: EventBus,
    ) -> None:
        super().__init__(repository._bus)
        self._repository = repository
        self._cache = cache
        self._cache_bus = cache_bus

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
            if ranking is not None:
                self._cache_bus.publish(_team_created_event(ranking))
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
            if ranking is not None:
                self._cache_bus.publish(_team_created_event(ranking))
        return ranking


def _team_created_event(ranking: Ranking[TeamID]) -> TeamRankingCalculatedEvent:
    return TeamRankingCalculatedEvent(
        ranking.id_.value,
        ranking.name,
        ranking.season_id.value,
        ranking.week,
        [
            EventValue(value.id_.value, value.order, value.rank, value.value)
            for value in ranking.values
        ],
    )


class TeamRankingEventHandler(BaseTeamEventHandler):
    def __init__(
        self,
        events: List[Event],
        event_bus: EventBus,
        cache_bus: EventBus,
    ) -> None:
        super().__init__(event_bus)
        self._events = events
        self._cache_bus = cache_bus

    def handle_calculated(self, event: TeamRankingCalculatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)


class GameRankingRepository(BaseGameRepository):
    def __init__(
        self,
        repository: BaseGameRepository,
        cache: MemoryGameRepository,
        cache_bus: EventBus,
    ) -> None:
        super().__init__(repository._bus)
        self._repository = repository
        self._cache = cache
        self._cache_bus = cache_bus

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
            if ranking is not None:
                self._cache_bus.publish(_game_created_event(ranking))
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
            if ranking is not None:
                self._cache_bus.publish(_game_created_event(ranking))
        return ranking


def _game_created_event(ranking: Ranking[GameID]) -> GameRankingCalculatedEvent:
    return GameRankingCalculatedEvent(
        ranking.id_.value,
        ranking.name,
        ranking.season_id.value,
        ranking.week,
        [
            EventValue(value.id_.value, value.order, value.rank, value.value)
            for value in ranking.values
        ],
    )


class GameRankingEventHandler(BaseGameEventHandler):
    def __init__(
        self,
        events: List[Event],
        event_bus: EventBus,
        cache_bus: EventBus,
    ) -> None:
        super().__init__(event_bus)
        self._events = events
        self._cache_bus = cache_bus

    def handle_calculated(self, event: GameRankingCalculatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)
