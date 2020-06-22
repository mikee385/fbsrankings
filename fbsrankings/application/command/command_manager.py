from types import TracebackType
from typing import Dict, Optional, Type
from typing_extensions import Literal

from fbsrankings.common import Command, CommandHandler, CommandBus, EventBus
from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.application.command import ImportSeasonByYearCommandHandler
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure.sportsreference import SportsReference


class CommandManager (object):
    def __init__(self, sports_reference: SportsReference, data_source: TransactionFactory, command_bus: CommandBus, event_bus: EventBus) -> None:
        self._bus = command_bus
        self._handlers = {}  # type: Dict[Type[Command], CommandHandler]
        
        self.register_hander(ImportSeasonByYearCommand, ImportSeasonByYearCommandHandler(sports_reference, data_source, event_bus))

    def register_hander(self, command: Type[Command], handler: CommandHandler) -> None:
        self._handlers[command] = handler
        self._bus.register_handler(command, handler)
        
    def close(self) -> None:
        for command, handler in self._handlers.items():
            self._bus.unregister_handler(command, handler)
    
    def __enter__(self) -> 'CommandManager':
        return self
        
    def __exit__(self, type: Optional[Type[BaseException]], value: Optional[BaseException], traceback: Optional[TracebackType]) -> Literal[False]:
        self.close()
        return False
