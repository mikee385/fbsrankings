from fbsrankings.common import EventBus
from fbsrankings.common import EventRecorder
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
        self._bus = EventRecorder(bus)

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
        for event in self._bus.events:
            handled = False

            handled = self._season.handle(event) or handled
            handled = self._team.handle(event) or handled
            handled = self._affiliation.handle(event) or handled
            handled = self._game.handle(event) or handled
            handled = self._team_record.handle(event) or handled
            handled = self._team_ranking.handle(event) or handled
            handled = self._game_ranking.handle(event) or handled

            if not handled:
                raise ValueError(f"Unknown event type: {type(event)}")

        self._bus.clear()

    def rollback(self) -> None:
        self._bus.clear()

    def close(self) -> None:
        self._bus.clear()
