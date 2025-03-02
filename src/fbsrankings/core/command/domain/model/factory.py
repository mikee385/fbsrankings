from communication.bus import EventBus
from fbsrankings.core.command.domain.model.affiliation import AffiliationFactory
from fbsrankings.core.command.domain.model.game import GameFactory
from fbsrankings.core.command.domain.model.season import SeasonFactory
from fbsrankings.core.command.domain.model.team import TeamFactory


class Factory:
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

        self._season = SeasonFactory(self._bus)
        self._team = TeamFactory(self._bus)
        self._affiliation = AffiliationFactory(self._bus)
        self._game = GameFactory(self._bus)

    @property
    def season(self) -> SeasonFactory:
        return self._season

    @property
    def team(self) -> TeamFactory:
        return self._team

    @property
    def affiliation(self) -> AffiliationFactory:
        return self._affiliation

    @property
    def game(self) -> GameFactory:
        return self._game
