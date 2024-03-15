from abc import ABCMeta
from abc import abstractmethod

from typing_extensions import Protocol

from fbsrankings.common import EventBus
from fbsrankings.ranking.command.domain.model.ranking import GameRankingRepository
from fbsrankings.ranking.command.domain.model.ranking import TeamRankingRepository
from fbsrankings.ranking.command.domain.model.record import TeamRecordRepository


class Repository(metaclass=ABCMeta):
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
