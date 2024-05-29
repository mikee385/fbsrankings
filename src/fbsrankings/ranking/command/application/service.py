from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.ranking.command.application.calculate_rankings_for_season import (
    CalculateRankingsForSeasonCommandHandler,
)
from fbsrankings.ranking.command.infrastructure.data_source import DataSource
from fbsrankings.shared.command import CalculateRankingsForSeasonCommand
from fbsrankings.shared.context import Context
from fbsrankings.shared.messaging import CommandBus
from fbsrankings.shared.messaging import EventBus
from fbsrankings.shared.messaging import QueryBus


class Service(ContextManager["Service"]):
    def __init__(
        self,
        context: Context,
        command_bus: CommandBus,
        query_bus: QueryBus,
        event_bus: EventBus,
    ) -> None:
        super().__init__()
        data_source = DataSource(context)

        self._command_bus = command_bus
        self._command_bus.register_handler(
            CalculateRankingsForSeasonCommand,
            CalculateRankingsForSeasonCommandHandler(
                data_source,
                query_bus,
                event_bus,
            ),
        )

    def close(self) -> None:
        self._command_bus.unregister_handler(CalculateRankingsForSeasonCommand)

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
