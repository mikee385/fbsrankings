from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ImportSeasonByYearCommand(_message.Message):
    __slots__ = ("command_id", "year")
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    command_id: str
    year: int
    def __init__(self, command_id: _Optional[str] = ..., year: _Optional[int] = ...) -> None: ...
