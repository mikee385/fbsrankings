from abc import ABCMeta
from abc import abstractmethod
from typing import Protocol

from communication.bus import EventBus
from fbsrankings.core.command.domain.model.affiliation import AffiliationRepository
from fbsrankings.core.command.domain.model.game import GameRepository
from fbsrankings.core.command.domain.model.season import SeasonRepository
from fbsrankings.core.command.domain.model.team import TeamRepository


class Repository(metaclass=ABCMeta):
    @property
    @abstractmethod
    def season(self) -> SeasonRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def team(self) -> TeamRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def affiliation(self) -> AffiliationRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def game(self) -> GameRepository:
        raise NotImplementedError


class RepositoryFactory(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def repository(self, event_bus: EventBus) -> Repository:
        raise NotImplementedError
