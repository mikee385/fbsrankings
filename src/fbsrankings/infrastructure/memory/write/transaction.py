from typing import List

from fbsrankings.common import Event
from fbsrankings.common import EventBus
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
from fbsrankings.infrastructure import Transaction as BaseTransaction
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.infrastructure.memory.write.affiliation import AffiliationRepository
from fbsrankings.infrastructure.memory.write.game import GameRepository
from fbsrankings.infrastructure.memory.write.ranking import GameRankingRepository
from fbsrankings.infrastructure.memory.write.ranking import TeamRankingRepository
from fbsrankings.infrastructure.memory.write.record import TeamRecordRepository
from fbsrankings.infrastructure.memory.write.season import SeasonRepository
from fbsrankings.infrastructure.memory.write.team import TeamRepository


class Transaction(BaseTransaction):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._bus = bus

        self._season = SeasonRepository(storage.season, self._bus)
        self._team = TeamRepository(storage.team, self._bus)
        self._affiliation = AffiliationRepository(storage.affiliation, self._bus)
        self._game = GameRepository(storage.game, self._bus)

        self._team_record = TeamRecordRepository(storage.team_record, self._bus)
        self._team_ranking = TeamRankingRepository(storage.team_ranking, self._bus)
        self._game_ranking = GameRankingRepository(storage.game_ranking, self._bus)

        self._events: List[Event] = []

        self._bus.register_handler(SeasonCreatedEvent, self._save_event)
        self._bus.register_handler(TeamCreatedEvent, self._save_event)
        self._bus.register_handler(AffiliationCreatedEvent, self._save_event)
        self._bus.register_handler(GameCreatedEvent, self._save_event)
        self._bus.register_handler(GameRescheduledEvent, self._save_event)
        self._bus.register_handler(GameCanceledEvent, self._save_event)
        self._bus.register_handler(GameCompletedEvent, self._save_event)
        self._bus.register_handler(GameNotesUpdatedEvent, self._save_event)
        self._bus.register_handler(TeamRecordCalculatedEvent, self._save_event)
        self._bus.register_handler(TeamRankingCalculatedEvent, self._save_event)
        self._bus.register_handler(GameRankingCalculatedEvent, self._save_event)

    def close(self) -> None:
        self._bus.unregister_handler(SeasonCreatedEvent, self._save_event)
        self._bus.unregister_handler(TeamCreatedEvent, self._save_event)
        self._bus.unregister_handler(AffiliationCreatedEvent, self._save_event)
        self._bus.unregister_handler(GameCreatedEvent, self._save_event)
        self._bus.unregister_handler(GameRescheduledEvent, self._save_event)
        self._bus.unregister_handler(GameCanceledEvent, self._save_event)
        self._bus.unregister_handler(GameCompletedEvent, self._save_event)
        self._bus.unregister_handler(GameNotesUpdatedEvent, self._save_event)
        self._bus.unregister_handler(TeamRecordCalculatedEvent, self._save_event)
        self._bus.unregister_handler(TeamRankingCalculatedEvent, self._save_event)
        self._bus.unregister_handler(GameRankingCalculatedEvent, self._save_event)

        self._events = []

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
        for event in self._events:
            if isinstance(event, SeasonCreatedEvent):
                self._season.handle_created(event)
            elif isinstance(event, TeamCreatedEvent):
                self._team.handle_created(event)
            elif isinstance(event, AffiliationCreatedEvent):
                self._affiliation.handle_created(event)
            elif isinstance(event, GameCreatedEvent):
                self._game.handle_created(event)
            elif isinstance(event, GameRescheduledEvent):
                self._game.handle_rescheduled(event)
            elif isinstance(event, GameCanceledEvent):
                self._game.handle_canceled(event)
            elif isinstance(event, GameCompletedEvent):
                self._game.handle_completed(event)
            elif isinstance(event, GameNotesUpdatedEvent):
                self._game.handle_notes_updated(event)
            elif isinstance(event, TeamRecordCalculatedEvent):
                self._team_record.handle_calculated(event)
            elif isinstance(event, TeamRankingCalculatedEvent):
                self._team_ranking.handle_calculated(event)
            elif isinstance(event, GameRankingCalculatedEvent):
                self._game_ranking.handle_calculated(event)

        self._events = []

    def rollback(self) -> None:
        self._events = []

    def _save_event(self, event: Event) -> None:
        self._events.append(event)
