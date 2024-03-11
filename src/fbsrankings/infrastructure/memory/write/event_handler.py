from fbsrankings.common import EventBus
from fbsrankings.infrastructure.event_handler import EventHandler as BaseEventHandler
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.infrastructure.memory.write.affiliation import AffiliationEventHandler
from fbsrankings.infrastructure.memory.write.game import GameEventHandler
from fbsrankings.infrastructure.memory.write.ranking import GameRankingEventHandler
from fbsrankings.infrastructure.memory.write.ranking import TeamRankingEventHandler
from fbsrankings.infrastructure.memory.write.record import TeamRecordEventHandler
from fbsrankings.infrastructure.memory.write.season import SeasonEventHandler
from fbsrankings.infrastructure.memory.write.team import TeamEventHandler


class EventHandler(BaseEventHandler):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._season = SeasonEventHandler(storage.season, bus)
        self._team = TeamEventHandler(storage.team, bus)
        self._affiliation = AffiliationEventHandler(storage.affiliation, bus)
        self._game = GameEventHandler(storage.game, bus)

        self._team_record = TeamRecordEventHandler(storage.team_record, bus)
        self._team_ranking = TeamRankingEventHandler(storage.team_ranking, bus)
        self._game_ranking = GameRankingEventHandler(storage.game_ranking, bus)

    def close(self) -> None:
        self._season.close()
        self._team.close()
        self._affiliation.close()
        self._game.close()

        self._team_record.close()
        self._team_ranking.close()
        self._game_ranking.close()
