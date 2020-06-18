from fbsrankings.common import EventBus
from fbsrankings.infrastructure import UnitOfWork
from fbsrankings.infrastructure.sportsreference import SportsReference


class ImportSeasonByYearCommandHandler (object):
    def __init__(self, sports_reference, data_source, event_bus):
        if not isinstance(sports_reference, SportsReference):
            raise TypeError('sports_reference must be of type SportsReference')
        self._sports_reference = sports_reference
        
        self._data_source = data_source
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
    def handle(self, command):
        with UnitOfWork(self._data_source, self._event_bus) as unit_of_work:
            self._sports_reference.import_season(command.year, unit_of_work)
        
            unit_of_work.commit()
