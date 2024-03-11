from typing import List

from fbsrankings.common import Event
from fbsrankings.common import EventBus
from fbsrankings.infrastructure.event_handler import EventHandler as BaseEventHandler
from fbsrankings.infrastructure.unit_of_work.affiliation import AffiliationEventHandler
from fbsrankings.infrastructure.unit_of_work.game import GameEventHandler
from fbsrankings.infrastructure.unit_of_work.ranking import GameRankingEventHandler
from fbsrankings.infrastructure.unit_of_work.ranking import TeamRankingEventHandler
from fbsrankings.infrastructure.unit_of_work.record import TeamRecordEventHandler
from fbsrankings.infrastructure.unit_of_work.season import SeasonEventHandler
from fbsrankings.infrastructure.unit_of_work.team import TeamEventHandler


class EventHandler(BaseEventHandler):
    def __init__(self, bus: EventBus) -> None:
        self.events: List[Event] = []

        self._season = SeasonEventHandler(self.events, bus)
        self._team = TeamEventHandler(self.events, bus)
        self._affiliation = AffiliationEventHandler(self.events, bus)
        self._game = GameEventHandler(self.events, bus)

        self._team_record = TeamRecordEventHandler(self.events, bus)
        self._team_ranking = TeamRankingEventHandler(self.events, bus)
        self._game_ranking = GameRankingEventHandler(self.events, bus)

    def close(self) -> None:
        self._season.close()
        self._team.close()
        self._affiliation.close()
        self._game.close()

        self._team_record.close()
        self._team_ranking.close()
        self._game_ranking.close()

        self.clear()

    def clear(self) -> None:
        self.events.clear()
