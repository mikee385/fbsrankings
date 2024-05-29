from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.core.command.application.import_season_by_year import (
    ImportSeasonByYearCommandHandler,
)
from fbsrankings.core.command.infrastructure.data_source import DataSource
from fbsrankings.shared.command import ImportSeasonByYearCommand
from fbsrankings.shared.context import Context
from fbsrankings.shared.messaging import CommandBus as BaseCommandBus
from fbsrankings.shared.messaging import EventBus


class CommandBus(BaseCommandBus, ContextManager["CommandBus"]):
    def __init__(self, context: Context, event_bus: EventBus) -> None:
        super().__init__()
        config = context.config
        data_source = DataSource(context)

        self.register_handler(
            ImportSeasonByYearCommand,
            ImportSeasonByYearCommandHandler(
                config,
                data_source,
                event_bus,
            ),
        )

    def close(self) -> None:
        self.unregister_handler(ImportSeasonByYearCommand)

    def __enter__(self) -> "CommandBus":
        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self.close()
        return False
