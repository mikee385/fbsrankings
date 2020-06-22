from typing import Callable, List, Dict, Type


class Event (object):
    pass


class EventBus (object):
    def __init__(self) -> None:
        self._handlers = {}  # type: Dict[Type[Event], List[Callable[[Event], None]]]
        
    def register_handler(self, type: Type[Event], handler: Callable[[Event], None]) -> None:
        existing = self._handlers.get(type)
        if existing is not None:
            existing.append(handler)
        else:
            self._handlers[type] = [handler]
        
    def publish(self, event: Event) -> None:
        handlers = self._handlers.get(type(event))
        if handlers is not None:
            for handler in handlers:
                handler(event)


class EventRecorder (EventBus):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus
        self.events = []  # type: List[Event]
        
    def register_handler(self, type: Type[Event], handler: Callable[[Event], None]) -> None:
        self._bus.register_handler(type, handler)
        
    def publish(self, event: Event) -> None:
        self.events.append(event)
        self._bus.publish(event)

    def clear(self) -> None:
        self.events = []
        

class EventCounter (EventBus):
    def __init__(self, bus: EventBus) -> None:
        self._bus = bus
        self.counts = {}  # type: Dict[Type[Event], int]
        
    def register_handler(self, type: Type[Event], handler: Callable[[Event], None]) -> None:
        self._bus.register_handler(type, handler)
        
    def publish(self, event: Event) -> None:
        count = self.counts.get(type(event))
        if count is None:
            self.counts[type(event)] = 1
        else:
            self.counts[type(event)] += 1
        self._bus.publish(event)

    def clear(self) -> None:
        self.counts = {}
