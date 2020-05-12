class Event (object):
    pass


class EventBus (object):
    def __init__(self):
        self._handlers = {}
        
    @property
    def types(self):
        return self._handlers.keys()
        
    def register_type(self, event_type):
        if not issubclass(event_type, Event):
            raise TypeError('event_type must be a type derived from Event')
        
        handlers = self._handlers.get(event_type)
        if handlers is None:
            self._handlers[event_type] = []
        
    def register_handler(self, event_type, handler):
        if not issubclass(event_type, Event):
            raise TypeError('event_type must be a type derived from Event')
        if not callable(handler):
            raise TypeError('handler must be a callable type')
        if event_type not in self._handlers:
            raise ValueError(f'Type {event_type.__name__} has not been registered with this EventBus')
            
        self._handlers[event_type].append(handler)
        
    def raise_event(self, event):
        if not isinstance(event, Event):
            raise TypeError('event must be of type Event')
        if type(event) not in self._handlers:
            raise ValueError(f'Type {type(event).__name__} has not been registered with this EventBus')
            
        for handler in self._handlers[type(event)]:
            handler(event)
            
            
class ReadOnlyEventBus (EventBus):
    def raise_event(self, event):
        raise ValueError('Domain should not have been modified')


class EventRecorder (EventBus):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        self.events = []
        
    @property
    def types(self):
        return self._event_bus.types
        
    def register_type(self, event_type):
        self._event_bus.register_type(event_type)
        
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
        
    @property
    def types(self):
        return self._event_bus.types
        
    def register_type(self, event_type):
        self._event_bus.register_type(event_type)
        
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
