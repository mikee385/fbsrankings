from uuid import UUID


class Identifier(object):
    def __init__(self, value: UUID) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Identifier):
            if isinstance(other, type(self)) or isinstance(self, type(other)):
                if isinstance(other.value, type(self.value)):
                    return self.value == other.value
                if isinstance(self.value, type(other.value)):
                    return other.value == self.value
                return NotImplemented
            return NotImplemented
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Identifier):
            if isinstance(other, type(self)) or isinstance(self, type(other)):
                if isinstance(other.value, type(self.value)):
                    return self.value != other.value
                if isinstance(self.value, type(other.value)):
                    return other.value != self.value
                return NotImplemented
            return NotImplemented
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Identifier):
            if isinstance(other, type(self)) or isinstance(self, type(other)):
                if isinstance(other.value, type(self.value)):
                    return self.value < other.value
                if isinstance(self.value, type(other.value)):
                    return other.value > self.value
                return NotImplemented
            return NotImplemented
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, Identifier):
            if isinstance(other, type(self)) or isinstance(self, type(other)):
                if isinstance(other.value, type(self.value)):
                    return self.value <= other.value
                if isinstance(self.value, type(other.value)):
                    return other.value >= self.value
                return NotImplemented
            return NotImplemented
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Identifier):
            if isinstance(other, type(self)) or isinstance(self, type(other)):
                if isinstance(other.value, type(self.value)):
                    return self.value > other.value
                if isinstance(self.value, type(other.value)):
                    return other.value < self.value
                return NotImplemented
            return NotImplemented
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Identifier):
            if isinstance(other, type(self)) or isinstance(self, type(other)):
                if isinstance(other.value, type(self.value)):
                    return self.value >= other.value
                if isinstance(self.value, type(other.value)):
                    return other.value <= self.value
                return NotImplemented
            return NotImplemented
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return str(self.value)
