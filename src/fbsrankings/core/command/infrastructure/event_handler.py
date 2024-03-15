from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal
from typing_extensions import Protocol

from fbsrankings.common import EventBus


class EventHandler(ContextManager["EventHandler"], metaclass=ABCMeta):
    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    def __enter__(self) -> "EventHandler":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False


class EventHandlerFactory(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def event_handler(self, event_bus: EventBus) -> EventHandler:
        raise NotImplementedError
