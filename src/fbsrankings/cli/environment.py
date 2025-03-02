from pathlib import Path
from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from communication.bridge import EventBridge
from communication.bus import CommandBus
from communication.bus import EventBus
from communication.bus import MemoryCommandBus
from communication.bus import MemoryEventBus
from communication.bus import MemoryQueryBus
from communication.bus import QueryBus
from communication.channel import MemoryEventChannel
from fbsrankings.config import ChannelType
from fbsrankings.config import Config
from fbsrankings.config import SerializationType
from fbsrankings.context import Context
from fbsrankings.core.command import Service as CoreCommandService
from fbsrankings.core.query import Service as CoreQueryService
from fbsrankings.messages.command import DropStorageCommand
from fbsrankings.ranking.command import Service as RankingCommandService
from fbsrankings.ranking.query import Service as RankingQueryService
from serialization import PickleSerializer


class Environment(ContextManager["Environment"]):
    def __init__(self, config_location: str) -> None:
        self.command_bus: CommandBus
        self.query_bus: QueryBus
        self.event_bus: EventBus

        package_dir = Path(__file__).resolve().parent.parent

        if config_location is not None:
            config_path = Path(config_location).resolve()
        else:
            config_path = package_dir / "fbsrankings.ini"
        if not config_path.is_file():
            raise ValueError(f"'{config_path}' must be a valid file path")

        config = Config.from_ini(config_path)
        self.context = Context(config)

        self.command_bus = MemoryCommandBus()
        self.query_bus = MemoryQueryBus()

        if config.serialization == SerializationType.NONE:
            self._serializer = None
        elif config.serialization == SerializationType.PICKLE:
            self._serializer = PickleSerializer()
        else:
            raise ValueError(f"Unknown serialization type: {config.serialization}")

        if config.channel == ChannelType.NONE:
            self.event_bus = MemoryEventBus()
        elif config.channel == ChannelType.MEMORY:
            if self._serializer is None:
                raise ValueError(
                    f"Serialization cannot be 'none' when channel is {config.channel}",
                )

            self._event_channel = MemoryEventChannel()
            self.event_bus = EventBridge(
                self._event_channel,
                self._serializer,
            )
        else:
            raise ValueError(f"Unknown channel type: {config.channel}")

        self.command_bus.register_handler(DropStorageCommand, self._drop_storage)

        self._core_command = CoreCommandService(
            self.context,
            self.command_bus,
            self.event_bus,
        )
        self._core_query = CoreQueryService(
            self.context,
            self.query_bus,
            self.event_bus,
        )

        self._ranking_command = RankingCommandService(
            self.context,
            self.command_bus,
            self.query_bus,
            self.event_bus,
        )
        self._ranking_query = RankingQueryService(
            self.context,
            self.query_bus,
            self.event_bus,
        )

    def _drop_storage(self, _: DropStorageCommand) -> None:
        self.context.drop_storage()

    def close(self) -> None:
        self._ranking_query.close()
        self._ranking_command.close()

        self._core_query.close()
        self._core_command.close()

        self.command_bus.unregister_handler(DropStorageCommand)
        self.context.close()

    def __enter__(self) -> "Environment":
        self.context.__enter__()

        self._core_command.__enter__()
        self._core_query.__enter__()

        self._ranking_command.__enter__()
        self._ranking_query.__enter__()

        return self

    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self._ranking_query.__exit__(type_, value, traceback)
        self._ranking_command.__exit__(type_, value, traceback)

        self._core_query.__exit__(type_, value, traceback)
        self._core_command.__exit__(type_, value, traceback)

        self.command_bus.unregister_handler(DropStorageCommand)
        self.context.__exit__(type_, value, traceback)

        return False
