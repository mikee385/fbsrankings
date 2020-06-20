from types import TracebackType
from typing import Optional, Type
from typing_extensions import Literal

from fbsrankings.common import EventBus
from fbsrankings.domain import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class Transaction (object):
    @property
    def season(self) -> SeasonRepository:
        raise NotImplementedError
        
    @property
    def team(self) -> TeamRepository:
        raise NotImplementedError
        
    @property
    def affiliation(self) -> AffiliationRepository:
        raise NotImplementedError
        
    @property
    def game(self) -> GameRepository:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError
        
    def rollback(self) -> None:
        raise NotImplementedError
        
    def close(self) -> None:
        raise NotImplementedError
    
    def __enter__(self) -> 'Transaction':
        return self
        
    def __exit__(self, type: Optional[Type[BaseException]], value: Optional[BaseException], traceback: Optional[TracebackType]) -> Literal[False]:
        self.close()
        return False


class TransactionFactory (object):
    def transaction(self, event_bus: EventBus) -> Transaction:
        raise NotImplementedError
