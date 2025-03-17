from typing import Optional
from uuid import uuid4

from communication.bus import EventBus
from communication.messages import Event
from fbsrankings.messages.event import GameRankingCalculatedEvent
from fbsrankings.messages.event import RankingValue as EventValue
from fbsrankings.messages.event import TeamRankingCalculatedEvent
from fbsrankings.ranking.command.domain.model.core import GameID
from fbsrankings.ranking.command.domain.model.core import SeasonID
from fbsrankings.ranking.command.domain.model.core import TeamID
from fbsrankings.ranking.command.domain.model.ranking import (
    GameRankingRepository as BaseGameRepository,
)
from fbsrankings.ranking.command.domain.model.ranking import Ranking
from fbsrankings.ranking.command.domain.model.ranking import RankingID
from fbsrankings.ranking.command.domain.model.ranking import (
    TeamRankingRepository as BaseTeamRepository,
)
from fbsrankings.ranking.command.infrastructure.memory.ranking import (
    GameRankingRepository as MemoryGameRepository,
)
from fbsrankings.ranking.command.infrastructure.memory.ranking import (
    TeamRankingRepository as MemoryTeamRepository,
)
from fbsrankings.ranking.command.infrastructure.shared.ranking import (
    GameRankingEventHandler as BaseGameEventHandler,
)
from fbsrankings.ranking.command.infrastructure.shared.ranking import (
    TeamRankingEventHandler as BaseTeamEventHandler,
)


class TeamRankingRepository(BaseTeamRepository):
    def __init__(
        self,
        repository: BaseTeamRepository,
        cache: MemoryTeamRepository,
        cache_bus: EventBus,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._cache_bus = cache_bus

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
        event_id=str(uuid4()),
        ranking_id=str(ranking.id_),
        name=ranking.name,
        season_id=str(ranking.season_id),
        week=ranking.week,
        values=[
            EventValue(
                id=str(value.id_),
                order=value.order,
                rank=value.rank,
                value=value.value,
            )
            for value in ranking.values
        ],
    )


class TeamRankingEventHandler(BaseTeamEventHandler):
    def __init__(
        self,
        events: list[Event],
        cache_bus: EventBus,
    ) -> None:
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
        self._repository = repository
        self._cache = cache
        self._cache_bus = cache_bus

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
        event_id=str(uuid4()),
        ranking_id=str(ranking.id_),
        name=ranking.name,
        season_id=str(ranking.season_id),
        week=ranking.week,
        values=[
            EventValue(
                id=str(value.id_),
                order=value.order,
                rank=value.rank,
                value=value.value,
            )
            for value in ranking.values
        ],
    )


class GameRankingEventHandler(BaseGameEventHandler):
    def __init__(
        self,
        events: list[Event],
        cache_bus: EventBus,
    ) -> None:
        self._events = events
        self._cache_bus = cache_bus

    def handle_calculated(self, event: GameRankingCalculatedEvent) -> None:
        self._events.append(event)
        self._cache_bus.publish(event)
