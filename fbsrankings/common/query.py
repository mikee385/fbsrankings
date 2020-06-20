from typing import Any, Dict, Type


class Query (object):
    pass


class QueryHandler (object):
    def handle(self, query: Query) -> Any:
        raise NotImplementedError
    

class QueryBus (object):
    def __init__(self) -> None:
        self._handlers: Dict[Type[Query], QueryHandler] = {}
        
    def register_handler(self, type: Type[Query], handler: QueryHandler) -> None:
        existing = self._handlers.get(type)
        if existing is not None:
            raise ValueError(f'A handler has already been registered for {type}')
        else:
            self._handlers[type] = handler
            
    def unregister_handler(self, type: Type[Query], handler: QueryHandler) -> None:
        self._handlers.pop(type)
        
    def query(self, query: Query) -> Any:
        handler = self._handlers.get(type(query))
        if handler is None:
            raise ValueError(f'No handler has been registered for {type(query)}')
        else:
            return handler.handle(query)
