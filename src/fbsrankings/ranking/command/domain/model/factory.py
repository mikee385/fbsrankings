from communication.bus import EventBus
from fbsrankings.ranking.command.domain.model.ranking import GameRankingFactory
from fbsrankings.ranking.command.domain.model.ranking import TeamRankingFactory
from fbsrankings.ranking.command.domain.model.record import TeamRecordFactory


class Factory:
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

        self._team_record = TeamRecordFactory(self._bus)
        self._team_ranking = TeamRankingFactory(self._bus)
        self._game_ranking = GameRankingFactory(self._bus)

    @property
    def team_record(self) -> TeamRecordFactory:
        return self._team_record

    @property
    def team_ranking(self) -> TeamRankingFactory:
        return self._team_ranking

    @property
    def game_ranking(self) -> GameRankingFactory:
        return self._game_ranking
