import sqlite3

from fbsrankings.common import EventBus
from fbsrankings.infrastructure import Repository as BaseRepository
from fbsrankings.infrastructure.sqlite.write.affiliation import AffiliationRepository
from fbsrankings.infrastructure.sqlite.write.game import GameRepository
from fbsrankings.infrastructure.sqlite.write.ranking import GameRankingRepository
from fbsrankings.infrastructure.sqlite.write.ranking import TeamRankingRepository
from fbsrankings.infrastructure.sqlite.write.record import TeamRecordRepository
from fbsrankings.infrastructure.sqlite.write.season import SeasonRepository
from fbsrankings.infrastructure.sqlite.write.team import TeamRepository


class Repository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection, bus: EventBus) -> None:
        self._season = SeasonRepository(connection, bus)
        self._team = TeamRepository(connection, bus)
        self._affiliation = AffiliationRepository(connection, bus)
        self._game = GameRepository(connection, bus)

        self._team_record = TeamRecordRepository(connection, bus)
        self._team_ranking = TeamRankingRepository(connection, bus)
        self._game_ranking = GameRankingRepository(connection, bus)

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
