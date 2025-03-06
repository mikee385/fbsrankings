from abc import ABCMeta
from abc import abstractmethod
from typing import Callable
from typing import Generic
from typing import Type
from typing import TypeVar
from uuid import UUID

from typing_extensions import Protocol


R = TypeVar("R", covariant=True)
Q = TypeVar("Q", contravariant=True)


class Query(Generic[R], Protocol):
    query_id: UUID


QueryHandler = Callable[[Q], R]


class QueryBus(metaclass=ABCMeta):
    @abstractmethod
    def register_handler(self, type_: Type[Q], handler: QueryHandler[Q, R]) -> None:
        raise NotImplementedError

    @abstractmethod
    def unregister_handler(self, type_: Type[Q]) -> None:
        raise NotImplementedError

    @abstractmethod
    def query(self, query: Query[R]) -> R:
        raise NotImplementedError
