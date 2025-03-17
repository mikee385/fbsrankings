import json
from dataclasses import asdict
from dataclasses import is_dataclass
from typing import Any
from typing import cast
from typing import TypeVar

from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse
from google.protobuf.message import Message

from serialization.domain.serializer import Serializer


T = TypeVar("T")


def default_encoder(o: Any) -> Any:
    if is_dataclass(o) and not isinstance(o, type):
        return asdict(o)
    return o


class JsonSerializer(Serializer):
    def serialize(self, item: T) -> bytes:
        if isinstance(item, Message):
            return MessageToJson(item).encode("utf-8")

        return json.dumps(item, default=default_encoder).encode("utf-8")

    def deserialize(self, data: bytes, type_: type[T]) -> T:
        json_str = data.decode("utf-8")
        if issubclass(type_, Message):
            return cast(T, Parse(json_str, type_()))

        return cast(T, json.loads(json_str))
