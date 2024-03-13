from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.domain import AffiliationRepository
from fbsrankings.domain import GameRankingRepository
from fbsrankings.domain import GameRepository
from fbsrankings.domain import SeasonRepository
from fbsrankings.domain import TeamRankingRepository
from fbsrankings.domain import TeamRecordRepository
from fbsrankings.domain import TeamRepository
from fbsrankings.infrastructure.data_source import DataSource
from fbsrankings.infrastructure.memory.storage import Storage as MemoryStorage
from fbsrankings.infrastructure.memory.write import EventHandler as MemoryEventHandler
from fbsrankings.infrastructure.memory.write import Repository as MemoryRepository
from fbsrankings.infrastructure.unit_of_work.event_handler import EventHandler
from fbsrankings.infrastructure.unit_of_work.repository import Repository


class UnitOfWork(ContextManager["UnitOfWork"]):
    def __init__(self, data_source: DataSource, bus: EventBus) -> None:
        self._data_source = data_source
        self._outer_bus = bus
        self._inner_bus = EventBus()

        self._data_repository = self._data_source.repository(self._inner_bus)

        self._cache_bus = EventBus()
        self._cache_storage = MemoryStorage()
        self._cache_repository = MemoryRepository(self._cache_storage, self._inner_bus)
        self._cache_handler = MemoryEventHandler(self._cache_storage, self._cache_bus)

        self._repository = Repository(
            self._data_repository,
            self._cache_repository,
            self._cache_bus,
        )
        self._event_handler = EventHandler(self._inner_bus, self._cache_bus)

    @property
    def season(self) -> SeasonRepository:
        return self._repository.season

    @property
    def team(self) -> TeamRepository:
        return self._repository.team

    @property
    def affiliation(self) -> AffiliationRepository:
        return self._repository.affiliation

    @property
    def game(self) -> GameRepository:
        return self._repository.game

    @property
    def team_record(self) -> TeamRecordRepository:
        return self._repository.team_record

    @property
    def team_ranking(self) -> TeamRankingRepository:
        return self._repository.team_ranking

    @property
    def game_ranking(self) -> GameRankingRepository:
        return self._repository.game_ranking

    def commit(self) -> None:
        storage_bus = EventBus()
        with self._data_source.event_handler(storage_bus) as event_handler:
            for event in self._event_handler.events:
                storage_bus.publish(event)
            event_handler.close()

        for event in self._event_handler.events:
            self._outer_bus.publish(event)

        self._cache_storage.drop()
        self._event_handler.clear()

    def rollback(self) -> None:
        self._cache_storage.drop()
        self._event_handler.clear()

    def close(self) -> None:
        self._cache_handler.close()
        self._cache_storage.drop()

        self._event_handler.close()
        self._event_handler.clear()

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
