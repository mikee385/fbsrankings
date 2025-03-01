import pickle
from typing import cast
from typing import Type
from typing import TypeVar

from fbsrankings.serialization.domain.serializer import Serializer


T = TypeVar("T")


class PickleSerializer(Serializer):
    def serialize(self, item: T) -> bytes:
        return pickle.dumps(item)

    def deserialize(self, data: bytes, type_: Type[T]) -> T:
        return cast(T, pickle.loads(data))
