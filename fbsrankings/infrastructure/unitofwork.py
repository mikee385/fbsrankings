class UnitOfWork (object):
    def commit(self):
        raise NotImplementedError
        

class UnitOfWorkFactory (object):
    def unit_of_work(self, event_bus):
        raise NotImplementedError
