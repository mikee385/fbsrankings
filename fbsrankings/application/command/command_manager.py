from types import TracebackType
from typing import Any, Dict, Optional, Type, TypeVar

from typing_extensions import ContextManager, Literal

from fbsrankings.application.command.import_season_by_year import (
    ImportSeasonByYearCommandHandler,
)
from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.common import Command, CommandBus, CommandHandler, EventBus
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure.sportsreference import SportsReference

C = TypeVar("C", bound=Command)


class CommandManager(ContextManager["CommandManager"]):
    def __init__(
        self,
        sports_reference: SportsReference,
        data_source: TransactionFactory,
        command_bus: CommandBus,
        event_bus: EventBus,
    ) -> None:
        self._bus = command_bus
        self._handlers: Dict[Type[Command], CommandHandler[Any]] = {}

        self.register_hander(
            ImportSeasonByYearCommand,
            ImportSeasonByYearCommandHandler(sports_reference, data_source, event_bus),
        )

    def register_hander(self, type: Type[C], handler: CommandHandler[C]) -> None:
        self._handlers[type] = handler
        self._bus.register_handler(type, handler)

    def close(self) -> None:
        for type, handler in self._handlers.items():
            self._bus.unregister_handler(type, handler)

    def __enter__(self) -> "CommandManager":
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
