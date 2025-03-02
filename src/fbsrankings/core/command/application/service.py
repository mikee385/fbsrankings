from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from communication.bus import CommandBus
from communication.bus import EventBus
from fbsrankings.context import Context
from fbsrankings.core.command.application.import_season_by_year import (
    ImportSeasonByYearCommandHandler,
)
from fbsrankings.core.command.infrastructure.data_source import DataSource
from fbsrankings.messages.command import ImportSeasonByYearCommand


class Service(ContextManager["Service"]):
    def __init__(
        self,
        context: Context,
        command_bus: CommandBus,
        event_bus: EventBus,
    ) -> None:
        config = context.config
        data_source = DataSource(context)

        self._command_bus = command_bus
        self._command_bus.register_handler(
            ImportSeasonByYearCommand,
            ImportSeasonByYearCommandHandler(
                config,
                data_source,
                event_bus,
            ),
        )

    def close(self) -> None:
        self._command_bus.unregister_handler(ImportSeasonByYearCommand)

    def __enter__(self) -> "Service":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
