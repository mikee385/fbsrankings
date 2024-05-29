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
from fbsrankings.shared.messaging import CommandBus as BaseCommandBus
from fbsrankings.shared.messaging import EventBus
from fbsrankings.shared.messaging import QueryBus


class CommandBus(BaseCommandBus, ContextManager["CommandBus"]):
    def __init__(
        self,
        context: Context,
        core_query_bus: QueryBus,
        event_bus: EventBus,
    ) -> None:
        super().__init__()
        data_source = DataSource(context)

        self.register_handler(
            CalculateRankingsForSeasonCommand,
            CalculateRankingsForSeasonCommandHandler(
                data_source,
                core_query_bus,
                event_bus,
            ),
        )

    def close(self) -> None:
        self.unregister_handler(CalculateRankingsForSeasonCommand)

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
