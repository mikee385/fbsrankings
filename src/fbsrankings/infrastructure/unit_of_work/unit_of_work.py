from types import TracebackType
from typing import ContextManager
from typing import List
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.domain import AffiliationRepository
from fbsrankings.domain import GameRankingRepository
from fbsrankings.domain import GameRepository
from fbsrankings.domain import SeasonRepository
from fbsrankings.domain import TeamRankingRepository
from fbsrankings.domain import TeamRecordRepository
from fbsrankings.domain import TeamRepository
from fbsrankings.event import AffiliationCreatedEvent
from fbsrankings.event import GameCanceledEvent
from fbsrankings.event import GameCompletedEvent
from fbsrankings.event import GameCreatedEvent
from fbsrankings.event import GameNotesUpdatedEvent
from fbsrankings.event import GameRankingCalculatedEvent
from fbsrankings.event import GameRescheduledEvent
from fbsrankings.event import SeasonCreatedEvent
from fbsrankings.event import TeamCreatedEvent
from fbsrankings.event import TeamRankingCalculatedEvent
from fbsrankings.event import TeamRecordCalculatedEvent
from fbsrankings.infrastructure.transaction import TransactionFactory
from fbsrankings.infrastructure.unit_of_work.affiliation import (
    AffiliationRepository as UnitOfWorkAffilationRepository,
)
from fbsrankings.infrastructure.unit_of_work.game import (
    GameRepository as UnitOfWorkGameRepository,
)
from fbsrankings.infrastructure.unit_of_work.ranking import (
    GameRankingRepository as UnitOfWorkGameRankingRepository,
)
from fbsrankings.infrastructure.unit_of_work.ranking import (
    TeamRankingRepository as UnitOfWorkTeamRankingRepository,
)
from fbsrankings.infrastructure.unit_of_work.record import (
    TeamRecordRepository as UnitOfWorkTeamRecordRepository,
)
from fbsrankings.infrastructure.unit_of_work.season import (
    SeasonRepository as UnitOfWorkSeasonRepository,
)
from fbsrankings.infrastructure.unit_of_work.team import (
    TeamRepository as UnitOfWorkTeamRepository,
)


class UnitOfWork(ContextManager["UnitOfWork"]):
    def __init__(self, data_source: TransactionFactory, bus: EventBus) -> None:
        self._outer_bus = bus
        self._inner_bus = EventBus()

        self._events: List[Event] = []

        self._inner_bus.register_handler(SeasonCreatedEvent, self._save_event)
        self._inner_bus.register_handler(TeamCreatedEvent, self._save_event)
        self._inner_bus.register_handler(AffiliationCreatedEvent, self._save_event)
        self._inner_bus.register_handler(GameCreatedEvent, self._save_event)
        self._inner_bus.register_handler(GameRescheduledEvent, self._save_event)
        self._inner_bus.register_handler(GameCanceledEvent, self._save_event)
        self._inner_bus.register_handler(GameCompletedEvent, self._save_event)
        self._inner_bus.register_handler(GameNotesUpdatedEvent, self._save_event)
        self._inner_bus.register_handler(TeamRecordCalculatedEvent, self._save_event)
        self._inner_bus.register_handler(TeamRankingCalculatedEvent, self._save_event)
        self._inner_bus.register_handler(GameRankingCalculatedEvent, self._save_event)

        self._transaction = data_source.transaction(self._inner_bus)

        self._season = UnitOfWorkSeasonRepository(self._transaction.season)
        self._team = UnitOfWorkTeamRepository(self._transaction.team)
        self._affiliation = UnitOfWorkAffilationRepository(
            self._transaction.affiliation,
        )
        self._game = UnitOfWorkGameRepository(self._transaction.game)
        self._team_record = UnitOfWorkTeamRecordRepository(
            self._transaction.team_record,
        )
        self._team_ranking = UnitOfWorkTeamRankingRepository(
            self._transaction.team_ranking,
        )
        self._game_ranking = UnitOfWorkGameRankingRepository(
            self._transaction.game_ranking,
        )

    @property
    def season(self) -> SeasonRepository:
        return self._season

    @property
    def team(self) -> TeamRepository:
        return self._team

    @property
    def affiliation(self) -> AffiliationRepository:
        return self._affiliation

    @property
    def game(self) -> GameRepository:
        return self._game

    @property
    def team_record(self) -> TeamRecordRepository:
        return self._team_record

    @property
    def team_ranking(self) -> TeamRankingRepository:
        return self._team_ranking

    @property
    def game_ranking(self) -> GameRankingRepository:
        return self._game_ranking

    def commit(self) -> None:
        self._transaction.commit()

        for event in self._events:
            self._outer_bus.publish(event)
        self._events = []

    def rollback(self) -> None:
        self._transaction.rollback()
        self._events = []

    def close(self) -> None:
        self._transaction.close()
        self._events = []

    def __enter__(self) -> "UnitOfWork":
        self._transaction.__enter__()
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self._transaction.__exit__(type_, value, traceback)
        self._events = []
        return False

    def _save_event(self, event: Event) -> None:
        self._events.append(event)
