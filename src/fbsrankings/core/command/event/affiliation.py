from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type
from uuid import UUID

from dataclasses import dataclass
from typing_extensions import Literal

from fbsrankings.common import Event
from fbsrankings.common import EventBus


@dataclass(frozen=True)
class AffiliationCreatedEvent(Event):
    id_: UUID
    season_id: UUID
    team_id: UUID
    subdivision: str


class AffiliationEventHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle_created(self, event: AffiliationCreatedEvent) -> None:
        raise NotImplementedError


class AffiliationEventManager(ContextManager["AffiliationEventManager"]):
    def __init__(self, handler: AffiliationEventHandler, bus: EventBus) -> None:
        self._handler = handler
        self._bus = bus

        self._bus.register_handler(
            AffiliationCreatedEvent,
            self._handler.handle_created,
        )

    def close(self) -> None:
        self._bus.unregister_handler(
            AffiliationCreatedEvent,
            self._handler.handle_created,
        )

    def __enter__(self) -> "AffiliationEventManager":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
