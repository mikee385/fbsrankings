from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LatestSeasonWeekResult(_message.Message):
    __slots__ = ("season_id", "year", "week")
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    season_id: str
    year: int
    week: int
    def __init__(self, season_id: _Optional[str] = ..., year: _Optional[int] = ..., week: _Optional[int] = ...) -> None: ...

class LatestSeasonWeekQuery(_message.Message):
    __slots__ = ("query_id",)
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    def __init__(self, query_id: _Optional[str] = ...) -> None: ...
