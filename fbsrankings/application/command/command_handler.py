from fbsrankings.common import CommandBus, EventBus
from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.application.command import ImportSeasonByYearCommandHandler
from fbsrankings.infrastructure.sportsreference import SportsReference


class CommandHandler (object):
    def __init__(self, sports_reference, data_source, command_bus, event_bus):
        if not isinstance(sports_reference, SportsReference):
            raise TypeError('sports_reference must be of type SportsReference')
            
        if not isinstance(command_bus, CommandBus):
            raise TypeError('command_bus must be of type CommandBus')
        self._bus = command_bus
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
            
        self._handlers = {}
        self._handlers[ImportSeasonByYearCommand] = ImportSeasonByYearCommandHandler(sports_reference, data_source, event_bus)
        
        for command, handler in self._handlers.items():
            self._bus.register_handler(command, handler)
        
    def close(self):
        for command, handler in self._handlers.items():
            self._bus.unregister_handler(command, handler)
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False
