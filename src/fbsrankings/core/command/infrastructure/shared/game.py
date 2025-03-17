from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import ContextManager
from typing import Literal
from typing import Optional

from communication.bus import EventBus
from fbsrankings.messages.event import GameCanceledEvent
from fbsrankings.messages.event import GameCompletedEvent
from fbsrankings.messages.event import GameCreatedEvent
from fbsrankings.messages.event import GameNotesUpdatedEvent
from fbsrankings.messages.event import GameRescheduledEvent


class GameEventHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle_created(self, event: GameCreatedEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_rescheduled(self, event: GameRescheduledEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_canceled(self, event: GameCanceledEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_completed(self, event: GameCompletedEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        raise NotImplementedError


class GameEventManager(ContextManager["GameEventManager"]):
    def __init__(self, handler: GameEventHandler, bus: EventBus) -> None:
        self._handler = handler
        self._bus = bus

        self._bus.register_handler(GameCreatedEvent, self._handler.handle_created)
        self._bus.register_handler(
            GameRescheduledEvent,
            self._handler.handle_rescheduled,
        )
        self._bus.register_handler(GameCanceledEvent, self._handler.handle_canceled)
        self._bus.register_handler(GameCompletedEvent, self._handler.handle_completed)
        self._bus.register_handler(
            GameNotesUpdatedEvent,
            self._handler.handle_notes_updated,
        )

    def close(self) -> None:
        self._bus.unregister_handler(GameCreatedEvent, self._handler.handle_created)
        self._bus.unregister_handler(
            GameRescheduledEvent,
            self._handler.handle_rescheduled,
        )
        self._bus.unregister_handler(GameCanceledEvent, self._handler.handle_canceled)
        self._bus.unregister_handler(GameCompletedEvent, self._handler.handle_completed)
        self._bus.unregister_handler(
            GameNotesUpdatedEvent,
            self._handler.handle_notes_updated,
        )

    def __enter__(self) -> "GameEventManager":
        return self

    def __exit__(
        self,
        type_: Optional[type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
