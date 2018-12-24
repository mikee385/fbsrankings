class Identifier (object):
    def __init__(self, value):
        self.value = value
        
    def __eq__(self, other):
        if isinstance(other, type(self)) or isinstance(self, type(other)):
            if isinstance(other.value, type(self.value)):
                return self.value == other.value
            if isinstance(self.value, type(other.value)):
                return other.value == self.value
            return False
        return False
        
    def __ne__(self, other):
        return not self.__eq__(self, other)
        
    def __str__(self):
        return str(self.value)
        
    def __hash__(self):
        return hash(self.value)
