import pickle
from typing import cast
from typing import TypeVar

from serialization.domain.serializer import Serializer


T = TypeVar("T")


class PickleSerializer(Serializer):
    def serialize(self, item: T) -> bytes:
        return pickle.dumps(item)

    def deserialize(self, data: bytes, type_: type[T]) -> T:
        return cast(T, pickle.loads(data))
