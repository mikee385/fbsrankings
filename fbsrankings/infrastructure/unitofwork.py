class UnitOfWork (object):
    def commit(self):
        raise NotImplementedError
        

class UnitOfWorkFactory (object):
    def __enter__(self):
        raise NotImplementedError

    def __exit__(self):
        raise NotImplementedError

    def unit_of_work(self, event_bus):
        raise NotImplementedError
