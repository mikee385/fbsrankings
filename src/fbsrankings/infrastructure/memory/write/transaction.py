from typing import Callable
from typing import List
from typing import Type
from typing import TypeVar

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.infrastructure import Transaction as BaseTransaction
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.infrastructure.memory.write.affiliation import AffiliationRepository
from fbsrankings.infrastructure.memory.write.game import GameRepository
from fbsrankings.infrastructure.memory.write.ranking import GameRankingRepository
from fbsrankings.infrastructure.memory.write.ranking import TeamRankingRepository
from fbsrankings.infrastructure.memory.write.record import TeamRecordRepository
from fbsrankings.infrastructure.memory.write.season import SeasonRepository
from fbsrankings.infrastructure.memory.write.team import TeamRepository


E = TypeVar("E", bound=Event, contravariant=True)


EventHandler = Callable[[E], None]


class TransactionEventBus(EventBus):
    def __init__(self, bus: EventBus) -> None:
        super().__init__()

        self._publish_bus = bus
        self._commit_bus = EventBus()
        self._events: List[Event] = []

    def register_handler(self, type_: Type[E], handler: EventHandler[E]) -> None:
        self._commit_bus.register_handler(type_, handler)

    def publish(self, event: E) -> None:
        self._events.append(event)
        self._publish_bus.publish(event)

    def commit(self) -> None:
        for event in self._events:
            self._commit_bus.publish(event)
        self.close()

    def rollback(self) -> None:
        self.close()

    def close(self) -> None:
        self._events = []


class Transaction(BaseTransaction):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._bus = TransactionEventBus(bus)

        self._season = SeasonRepository(storage.season, self._bus)
        self._team = TeamRepository(storage.team, self._bus)
        self._affiliation = AffiliationRepository(storage.affiliation, self._bus)
        self._game = GameRepository(storage.game, self._bus)

        self._team_record = TeamRecordRepository(storage.team_record, self._bus)
        self._team_ranking = TeamRankingRepository(storage.team_ranking, self._bus)
        self._game_ranking = GameRankingRepository(storage.game_ranking, self._bus)

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
        self._bus.commit()
        self.close()

    def rollback(self) -> None:
        self._bus.rollback()
        self.close()

    def close(self) -> None:
        self._season.close()
        self._team.close()
        self._affiliation.close()
        self._game.close()

        self._team_record.close()
        self._team_ranking.close()
        self._game_ranking.close()

        self._bus.close()
