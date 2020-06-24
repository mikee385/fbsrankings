from abc import ABCMeta
from types import TracebackType
from typing import Any, Dict, Optional, Type, TypeVar

from typing_extensions import ContextManager, Literal, Protocol

from fbsrankings.common import QueryBus, QueryHandler

R = TypeVar("R", covariant=True)
Q = TypeVar("Q", contravariant=True)


class QueryManager(ContextManager["QueryManager"], metaclass=ABCMeta):
    def __init__(self, query_bus: QueryBus) -> None:
        self._bus = query_bus
        self._handlers: Dict[Type[Any], QueryHandler[Any, Any]] = {}

    def register_handler(self, type: Type[Q], handler: QueryHandler[Q, R]) -> None:
        self._handlers[type] = handler
        self._bus.register_handler(type, handler)

    def close(self) -> None:
        for type, handler in self._handlers.items():
            self._bus.unregister_handler(type, handler)

    def __enter__(self) -> "QueryManager":
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False


class QueryManagerFactory(Protocol):
    def query_manager(self, query_bus: QueryBus) -> QueryManager:
        raise NotImplementedError
