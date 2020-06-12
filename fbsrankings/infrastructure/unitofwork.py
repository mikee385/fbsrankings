class UnitOfWork (object):
    def commit(self):
        raise NotImplementedError
        

class UnitOfWorkFactory (object):
    def unit_of_work(self, bus):
        raise NotImplementedError
