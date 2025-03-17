from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CalculateRankingsForSeasonCommand(_message.Message):
    __slots__ = ("command_id", "season_id", "year")
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    command_id: str
    season_id: str
    year: int
    def __init__(self, command_id: _Optional[str] = ..., season_id: _Optional[str] = ..., year: _Optional[int] = ...) -> None: ...
