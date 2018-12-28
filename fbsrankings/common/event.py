class Event (object):
    pass


class EventBus (object):
    def __init__(self):
        self._handlers = {}
        
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
            raise ValueError('Type ' + event_type.__name__ + ' has not been registered with this EventBus')
            
        self._handlers[event_type].append(handler)
        
    def raise_event(self, event):
        if not isinstance(event, Event):
            raise TypeError('event must be of type Event')
        if type(event) not in self._handlers:
            raise ValueError('Type ' + type(event).__name__ + ' has not been registered with this EventBus')
            
        for handler in self._handlers[type(event)]:
            handler(event)
        
