from abc import ABCMeta
from abc import abstractmethod
from typing import Type

from communication.messages import Q
from communication.messages import Query
from communication.messages import QueryHandler
from communication.messages import R


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
