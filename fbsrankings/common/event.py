class Event (object):
    pass


class EventBus (object):
    def __init__(self):
        self._handlers = {}
        
    def register_handler(self, event_type, handler):
        if not issubclass(event_type, Event):
            raise TypeError('event_type must be a type derived from Event')
        if not callable(handler):
            raise TypeError('handler must be a callable type')
        
        handlers = self._handlers.get(event_type)
        if handlers is not None:
            handlers.append(handler)
        else:
            self._handlers[event_type] = [handler]
        
    def raise_event(self, event):
        if not isinstance(event, Event):
            raise TypeError('event must be of type Event')
        
        handlers = self._handlers.get(type(event))
        if handlers is not None:
            for handler in handlers:
                handler(event)
            
            
class ReadOnlyEventBus (EventBus):
    def raise_event(self, event):
        raise ValueError('Domain should not have been modified')
        

class LocalEventHandler (EventBus):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._global_bus = event_bus
        self._local_bus = EventBus()
        
    def register_handler(self, event_type, handler):
        self._local_bus.register_handler(event_type, handler)
        
    def raise_event(self, event):
        self._local_bus.raise_event(event)
        self._global_bus.raise_event(event)


class EventRecorder (EventBus):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        self.events = []
        
    def register_handler(self, event_type, handler):
        self._event_bus.register_handler(handler)
        
    def raise_event(self, event):
        self.events.append(event)
        self._event_bus.raise_event(event)

    def clear(self):
        self.events = []
        

class EventCounter (EventBus):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        self.counts = {}
        
    def register_handler(self, event_type, handler):
        self._event_bus.register_handler(handler)
        
    def raise_event(self, event):
        count = self.counts.get(type(event))
        if count is None:
            self.counts[type(event)] = 1
        else:
            self.counts[type(event)] += 1
        self._event_bus.raise_event(event)

    def clear(self):
        self.counts = {}
