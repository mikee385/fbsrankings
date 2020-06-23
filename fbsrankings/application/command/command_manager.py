from types import TracebackType
from typing import Dict, Optional, Type

from typing_extensions import ContextManager, Literal

from fbsrankings.application.command.import_season_by_year import (
    ImportSeasonByYearCommandHandler,
)
from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.common import Command, CommandBus, CommandHandler, EventBus
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure.sportsreference import SportsReference


class CommandManager(ContextManager["CommandManager"]):
    def __init__(
        self,
        sports_reference: SportsReference,
        data_source: TransactionFactory,
        command_bus: CommandBus,
        event_bus: EventBus,
    ) -> None:
        self._bus = command_bus
        self._handlers: Dict[Type[Command], CommandHandler] = {}

        self.register_hander(
            ImportSeasonByYearCommand,
            ImportSeasonByYearCommandHandler(sports_reference, data_source, event_bus),
        )

    def register_hander(self, command: Type[Command], handler: CommandHandler) -> None:
        self._handlers[command] = handler
        self._bus.register_handler(command, handler)

    def close(self) -> None:
        for command, handler in self._handlers.items():
            self._bus.unregister_handler(command, handler)

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
