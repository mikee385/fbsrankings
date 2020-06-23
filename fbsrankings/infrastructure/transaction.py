from abc import ABCMeta, abstractmethod
from types import TracebackType
from typing import Optional, Type

from typing_extensions import ContextManager, Literal, Protocol

from fbsrankings.common import EventBus
from fbsrankings.domain import (
    AffiliationRepository,
    GameRepository,
    SeasonRepository,
    TeamRepository,
)


class Transaction(ContextManager["Transaction"], metaclass=ABCMeta):
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

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    def __enter__(self) -> "Transaction":
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False


class TransactionFactory(Protocol):
    def transaction(self, event_bus: EventBus) -> Transaction:
        raise NotImplementedError
