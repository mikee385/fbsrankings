from types import TracebackType
from typing import Any
from typing import ContextManager
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar

from typing_extensions import Literal

from fbsrankings.command import CalculateRankingsForSeasonCommand
from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.common import Command
from fbsrankings.common import CommandBus
from fbsrankings.common import CommandHandler
from fbsrankings.common import EventBus
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure.sportsreference import SportsReference
from fbsrankings.service.command.calculate_rankings_for_season import (
    CalculateRankingsForSeasonCommandHandler,
)
from fbsrankings.service.command.import_season_by_year import (
    ImportSeasonByYearCommandHandler,
)

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

        self.register_hander(
            CalculateRankingsForSeasonCommand,
            CalculateRankingsForSeasonCommandHandler(data_source, event_bus),
        )

    def register_hander(self, type_: Type[C], handler: CommandHandler[C]) -> None:
        self._bus.register_handler(type_, handler)
        self._handlers[type_] = handler

    def close(self) -> None:
        for type_ in self._handlers:
            self._bus.unregister_handler(type_)

    def __enter__(self) -> "CommandManager":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
