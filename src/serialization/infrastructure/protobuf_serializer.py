from typing import cast
from typing import TypeVar

from google.protobuf.message import Message

from serialization.domain.serializer import Serializer


T = TypeVar("T")


class ProtobufSerializer(Serializer):
    def serialize(self, item: T) -> bytes:
        if isinstance(item, Message):
            return item.SerializeToString()

        raise TypeError(f"Object of type {type(item)} is not Protobuf serializable")

    def deserialize(self, data: bytes, type_: type[T]) -> T:
        if issubclass(type_, Message):
            item = type_()
            item.ParseFromString(data)
            return cast(T, item)

        raise TypeError(f"Object of type {type_} is not Protobuf serializable")
