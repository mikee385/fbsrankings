from fbsrankings.common import EventBus
from fbsrankings.core.command.infrastructure.event_handler import (
    EventHandler as BaseEventHandler,
)
from fbsrankings.core.command.infrastructure.memory.affiliation import (
    AffiliationEventHandler,
)
from fbsrankings.core.command.infrastructure.memory.game import GameEventHandler
from fbsrankings.core.command.infrastructure.memory.season import SeasonEventHandler
from fbsrankings.core.command.infrastructure.memory.team import TeamEventHandler
from fbsrankings.storage.memory import Storage


class EventHandler(BaseEventHandler):
    def __init__(self, storage: Storage, bus: EventBus) -> None:
        self._season = SeasonEventHandler(storage.season, bus)
        self._team = TeamEventHandler(storage.team, bus)
        self._affiliation = AffiliationEventHandler(storage.affiliation, bus)
        self._game = GameEventHandler(storage.game, bus)

    def close(self) -> None:
        self._season.close()
        self._team.close()
        self._affiliation.close()
        self._game.close()
