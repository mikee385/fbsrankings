from abc import ABCMeta
from abc import abstractmethod

from typing_extensions import Protocol

from fbsrankings.common import EventBus
from fbsrankings.domain import AffiliationRepository
from fbsrankings.domain import GameRankingRepository
from fbsrankings.domain import GameRepository
from fbsrankings.domain import SeasonRepository
from fbsrankings.domain import TeamRankingRepository
from fbsrankings.domain import TeamRecordRepository
from fbsrankings.domain import TeamRepository


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

    @property
    @abstractmethod
    def team_record(self) -> TeamRecordRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def team_ranking(self) -> TeamRankingRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def game_ranking(self) -> GameRankingRepository:
        raise NotImplementedError


class RepositoryFactory(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def repository(self, event_bus: EventBus) -> Repository:
        raise NotImplementedError
