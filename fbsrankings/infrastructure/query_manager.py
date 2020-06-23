from types import TracebackType
from typing import Any, Dict, Optional, Type, TypeVar

from typing_extensions import ContextManager, Literal, Protocol

from fbsrankings.common import Query, QueryBus, QueryHandler

Q = TypeVar("Q", bound=Query)


class QueryManager(ContextManager["QueryManager"]):
    def __init__(self, query_bus: QueryBus) -> None:
        self._bus = query_bus
        self._handlers: Dict[Type[Query], QueryHandler[Any]] = {}

    def register_hander(self, query: Type[Q], handler: QueryHandler[Q]) -> None:
        self._handlers[query] = handler
        self._bus.register_handler(query, handler)

    def close(self) -> None:
        for query, handler in self._handlers.items():
            self._bus.unregister_handler(query, handler)

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
