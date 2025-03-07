from typing import Any
from typing import cast
from typing import Dict
from typing import Type

from communication.bus.domain.query import QueryBus
from communication.messages import Q
from communication.messages import Query
from communication.messages import QueryHandler
from communication.messages import R


class MemoryQueryBus(QueryBus):
    def __init__(self) -> None:
        self._handlers: Dict[Type[Query[Any]], QueryHandler[Any, Any]] = {}

    def register_handler(self, type_: Type[Q], handler: QueryHandler[Q, R]) -> None:
        existing = self._handlers.get(type_)
        if existing is not None:
            raise ValueError(f"A handler has already been registered for {type_}")
        self._handlers[type_] = handler

    def unregister_handler(self, type_: Type[Q]) -> None:
        self._handlers.pop(type_)

    def query(self, query: Query[R]) -> R:
        handler = cast(QueryHandler[Query[R], R], self._handlers.get(type(query)))
        if handler is None:
            raise ValueError(f"No handler has been registered for {type(query)}")
        return handler(query)
