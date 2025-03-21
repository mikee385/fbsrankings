from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DropStorageCommand(_message.Message):
    __slots__ = ("command_id",)
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    command_id: str
    def __init__(self, command_id: _Optional[str] = ...) -> None: ...
