class Query (object):
    pass
    

class QueryBus (object):
    def __init__(self):
        self._handlers = {}
        
    def register_handler(self, type, handler):
        if not issubclass(type, Query):
            raise TypeError('type must be a type derived from Query')
        
        existing = self._handlers.get(type)
        if existing is not None:
            raise ValueError(f'A handler has already been registered for {type}')
        else:
            self._handlers[type] = handler
        
    def query(self, query):
        if not isinstance(query, Query):
            raise TypeError('query must be of type Query')
        
        handler = self._handlers.get(type(query))
        if handler is None:
            raise ValueError(f'No handler has been registered for {type(query)}')
        else:
            return handler.handle(query)
