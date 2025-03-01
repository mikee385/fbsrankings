from abc import ABCMeta
from abc import abstractmethod
from typing import Type
from typing import TypeVar


T = TypeVar("T")


class Serializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, item: T) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, data: bytes, type_: Type[T]) -> T:
        raise NotImplementedError
