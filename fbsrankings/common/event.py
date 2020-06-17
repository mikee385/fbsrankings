class Event (object):
    pass


class EventBus (object):
    def __init__(self):
        self._handlers = {}
        
    def register_handler(self, type, handler):
        if not issubclass(type, Event):
            raise TypeError('type must be a type derived from Event')
        if not callable(handler):
            raise TypeError('handler must be a callable type')
        
        existing = self._handlers.get(type)
        if existing is not None:
            existing.append(handler)
        else:
            self._handlers[type] = [handler]
        
    def publish(self, event):
        if not isinstance(event, Event):
            raise TypeError('event must be of type Event')
        
        handlers = self._handlers.get(type(event))
        if handlers is not None:
            for handler in handlers:
                handler(event)


class EventRecorder (EventBus):
    def __init__(self, bus):
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._bus = bus
        self.events = []
        
    def register_handler(self, type, handler):
        self._bus.register_handler(type, handler)
        
    def publish(self, event):
        self.events.append(event)
        self._bus.publish(event)

    def clear(self):
        self.events = []
        

class EventCounter (EventBus):
    def __init__(self, bus):
        if not isinstance(bus, EventBus):
            raise TypeError('bus must be of type EventBus')
        self._bus = bus
        self.counts = {}
        
    def register_handler(self, type, handler):
        self._bus.register_handler(type, handler)
        
    def publish(self, event):
        count = self.counts.get(type(event))
        if count is None:
            self.counts[type(event)] = 1
        else:
            self.counts[type(event)] += 1
        self._bus.publish(event)

    def clear(self):
        self.counts = {}
