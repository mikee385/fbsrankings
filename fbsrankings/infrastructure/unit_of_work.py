from fbsrankings.common import EventBus, EventRecorder


class UnitOfWork (object):
    def __init__(self, data_store, bus):
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._outer_bus = bus
        self._inner_bus = EventRecorder(EventBus())
        
        self._transaction = data_store.transaction(self._inner_bus)
        
    @property
    def season(self):
        return self._transaction.season
        
    @property
    def team(self):
        return self._transaction.team
        
    @property
    def affiliation(self):
        return self._transaction.affiliation
        
    @property
    def game(self):
        return self._transaction.game

    def commit(self):
        self._transaction.commit()
        
        for event in self._inner_bus.events:
            self._outer_bus.publish(event)
        self._inner_bus.clear()
        
    def rollback(self):
        self._transaction.rollback()
        self._inner_bus.clear()
        
    def close(self):
        self._transaction.close()
        self._inner_bus.clear()
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()
        return False
