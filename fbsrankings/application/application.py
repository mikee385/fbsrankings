from fbsrankings.application.command import CommandHandler
from fbsrankings.common import CommandBus, EventBus, QueryBus
from fbsrankings.domain import ValidationService, RaiseBehavior
from fbsrankings.infrastructure.sportsreference import SportsReference
from fbsrankings.infrastructure.memory import DataSource as MemoryDataSource
from fbsrankings.infrastructure.sqlite import DataSource as SqliteDataSource


class Application (object):
    def __init__(self, config, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        storage_type = config['settings']['storage_type']
        if storage_type == 'memory':
            self._data_source = MemoryDataSource()

        elif storage_type == 'sqlite':
            db_filename = config['settings']['sqlite_db_file']
            self._data_source = SqliteDataSource(db_filename)

        else:
            raise ValueError(f'Unknown storage type: {storage_type}')
                
        alternate_names = config.get('alternate_names')
        if alternate_names is None:
            alternate_names = {}
            
        self.validation_service = ValidationService(RaiseBehavior.ON_DEMAND)
            
        self.seasons = []
        self._sports_reference = SportsReference(alternate_names, self.validation_service)
        for season in config['seasons']:
            self.seasons.append(season['year'])
            self._sports_reference.add_source(
                season['year'],
                season['postseason_start_week'],
                season['source_type'],
                season['teams'],
                season['games']
            )
            
        self._command_bus = CommandBus()
        self._command_handler = CommandHandler(self._sports_reference, self._data_source, self._command_bus, self._event_bus)

        self._query_bus = QueryBus()
        self._query_handler = self._data_source.query_handler(self._query_bus)
        
    @property
    def errors(self):
        return self.validation_service.errors
        
    def send(self, command):
        self._command_bus.send(command)
        
    def query(self, query):
        return self._query_bus.query(query)
        
    def close(self):
        self._query_handler.close()
        self._command_handler.close()
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False
