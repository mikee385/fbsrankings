from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SeasonByYearResult(_message.Message):
    __slots__ = ("season_id", "year")
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    season_id: str
    year: int
    def __init__(self, season_id: _Optional[str] = ..., year: _Optional[int] = ...) -> None: ...

class SeasonByYearQuery(_message.Message):
    __slots__ = ("query_id", "year")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    year: int
    def __init__(self, query_id: _Optional[str] = ..., year: _Optional[int] = ...) -> None: ...
