from abc import ABCMeta
from abc import abstractmethod
from typing import Callable
from typing import Generic
from typing import Type
from typing import TypeVar


R = TypeVar("R", covariant=True)
Q = TypeVar("Q", contravariant=True)


class Query(Generic[R], metaclass=ABCMeta):  # noqa: B024
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
