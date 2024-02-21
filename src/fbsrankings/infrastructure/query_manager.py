from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import Any
from typing import ContextManager
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar

from typing_extensions import Literal
from typing_extensions import Protocol

from fbsrankings.common import QueryBus
from fbsrankings.common import QueryHandler

R = TypeVar("R", covariant=True)
Q = TypeVar("Q", contravariant=True)


class QueryManager(ContextManager["QueryManager"], metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, query_bus: QueryBus) -> None:
        self._bus = query_bus
        self._handlers: Dict[Type[Any], QueryHandler[Any, Any]] = {}

    def register_handler(self, type_: Type[Q], handler: QueryHandler[Q, R]) -> None:
        self._handlers[type_] = handler
        self._bus.register_handler(type_, handler)

    def close(self) -> None:
        for type_ in self._handlers:
            self._bus.unregister_handler(type_)

    def __enter__(self) -> "QueryManager":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False


class QueryManagerFactory(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def query_manager(self, query_bus: QueryBus) -> QueryManager:
        raise NotImplementedError
