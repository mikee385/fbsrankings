from fbsrankings.common import QueryBus, EventBus
from fbsrankings.domain import ValidationService, RaiseBehavior
from fbsrankings.infrastructure import UnitOfWork
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

        self._query_bus = QueryBus()
        self._query_handler = self._data_source.query_handler(self._query_bus)
        
    @property
    def errors(self):
        return self.validation_service.errors

    def import_season(self, year):
        with UnitOfWork(self._data_source, self._event_bus) as unit_of_work:
            self._sports_reference.import_season(year, unit_of_work)
        
            unit_of_work.commit()

    def calculate_rankings(self, year):
        pass
        
    def query(self, query):
        return self._query_bus.query(query)
        
    def close(self):
        self._query_handler.close()
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False
