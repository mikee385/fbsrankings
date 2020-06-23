from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Generic, Type, TypeVar


class Query(metaclass=ABCMeta):
    pass


Q = TypeVar("Q", bound=Query)


class QueryHandler(Generic[Q], metaclass=ABCMeta):
    @abstractmethod
    def handle(self, query: Q) -> Any:
        raise NotImplementedError


class QueryBus(object):
    def __init__(self) -> None:
        self._handlers: Dict[Type[Query], QueryHandler[Any]] = {}

    def register_handler(self, type: Type[Q], handler: QueryHandler[Q]) -> None:
        existing = self._handlers.get(type)
        if existing is not None:
            raise ValueError(f"A handler has already been registered for {type}")
        else:
            self._handlers[type] = handler

    def unregister_handler(self, type: Type[Q], handler: QueryHandler[Q]) -> None:
        self._handlers.pop(type)

    def query(self, query: Q) -> Any:
        handler = self._handlers.get(type(query))
        if handler is None:
            raise ValueError(f"No handler has been registered for {type(query)}")
        else:
            return handler.handle(query)
