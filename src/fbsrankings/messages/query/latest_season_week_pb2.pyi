from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LatestSeasonWeekValue(_message.Message):
    __slots__ = ("season_id", "year", "week")
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    season_id: str
    year: int
    week: int
    def __init__(self, season_id: _Optional[str] = ..., year: _Optional[int] = ..., week: _Optional[int] = ...) -> None: ...

class LatestSeasonWeekResult(_message.Message):
    __slots__ = ("query_id", "latest")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    LATEST_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    latest: LatestSeasonWeekValue
    def __init__(self, query_id: _Optional[str] = ..., latest: _Optional[_Union[LatestSeasonWeekValue, _Mapping]] = ...) -> None: ...

class LatestSeasonWeekQuery(_message.Message):
    __slots__ = ("query_id",)
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    def __init__(self, query_id: _Optional[str] = ...) -> None: ...
