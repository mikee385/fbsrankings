from abc import ABCMeta
from abc import abstractmethod
from typing import Callable
from typing import Generic
from typing import Type
from typing import TypeVar
from uuid import UUID

from typing_extensions import Protocol


class QueryBase(Protocol):
    query_id: UUID


Q = TypeVar("Q", bound=QueryBase, contravariant=True)
R = TypeVar("R", covariant=True)


class Query(QueryBase, Generic[R], Protocol):
    pass


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
