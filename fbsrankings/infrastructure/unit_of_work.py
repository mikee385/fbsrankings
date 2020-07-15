from types import TracebackType
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.common import EventRecorder
from fbsrankings.domain import AffiliationRepository
from fbsrankings.domain import GameRankingRepository
from fbsrankings.domain import GameRepository
from fbsrankings.domain import SeasonRepository
from fbsrankings.domain import TeamRankingRepository
from fbsrankings.domain import TeamRepository
from fbsrankings.infrastructure.transaction import TransactionFactory


class UnitOfWork:
    def __init__(self, data_source: TransactionFactory, bus: EventBus) -> None:
        self._outer_bus = bus
        self._inner_bus = EventRecorder(EventBus())

        self._transaction = data_source.transaction(self._inner_bus)

    @property
    def season(self) -> SeasonRepository:
        return self._transaction.season

    @property
    def team(self) -> TeamRepository:
        return self._transaction.team

    @property
    def affiliation(self) -> AffiliationRepository:
        return self._transaction.affiliation

    @property
    def game(self) -> GameRepository:
        return self._transaction.game

    @property
    def team_ranking(self) -> TeamRankingRepository:
        return self._transaction.team_ranking

    @property
    def game_ranking(self) -> GameRankingRepository:
        return self._transaction.game_ranking

    def commit(self) -> None:
        self._transaction.commit()

        for event in self._inner_bus.events:
            self._outer_bus.publish(event)
        self._inner_bus.clear()

    def rollback(self) -> None:
        self._transaction.rollback()
        self._inner_bus.clear()

    def close(self) -> None:
        self._transaction.close()
        self._inner_bus.clear()

    def __enter__(self) -> "UnitOfWork":
        self._transaction.__enter__()
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self._transaction.__exit__(type, value, traceback)
        self._inner_bus.clear()
        return False
