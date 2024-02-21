from abc import ABCMeta
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import Generic
from typing import Type
from typing import TypeVar

R = TypeVar("R", covariant=True)
Q = TypeVar("Q", contravariant=True)


class Query(Generic[R], metaclass=ABCMeta):  # noqa: B024
    pass


QueryHandler = Callable[[Q], R]


class QueryBus:
    def __init__(self) -> None:
        self._handlers: Dict[Type[Any], QueryHandler[Any, Any]] = {}

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
