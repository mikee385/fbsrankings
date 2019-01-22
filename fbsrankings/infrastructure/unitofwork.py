from fbsrankings.common import EventBus


class UnitOfWork (object):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self.event_bus = event_bus

    def commit(self):
        raise NotImplementedError
        

class UnitOfWorkFactory (object):
    def create(self, event_bus):
        raise NotImplementedError
