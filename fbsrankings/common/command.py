class Command (object):
    pass
    

class CommandBus (object):
    def __init__(self):
        self._handlers = {}
        
    def register_handler(self, type, handler):
        if not issubclass(type, Command):
            raise TypeError('type must be a type derived from Command')
        
        existing = self._handlers.get(type)
        if existing is not None:
            raise ValueError(f'A handler has already been registered for {type}')
        else:
            self._handlers[type] = handler
            
    def unregister_handler(self, type, handler):
        self._handlers.pop(type)
            
    def send(self, command):
        if not isinstance(command, Command):
            raise TypeError('command must be of type Command')
        
        handler = self._handlers.get(type(command))
        if handler is None:
            raise ValueError(f'No handler has been registered for {type(command)}')
        else:
            handler.handle(command)
