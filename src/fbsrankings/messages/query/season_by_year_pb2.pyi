from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SeasonByYearValue(_message.Message):
    __slots__ = ("season_id", "year")
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    season_id: str
    year: int
    def __init__(self, season_id: _Optional[str] = ..., year: _Optional[int] = ...) -> None: ...

class SeasonByYearResult(_message.Message):
    __slots__ = ("query_id", "season")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    season: SeasonByYearValue
    def __init__(self, query_id: _Optional[str] = ..., season: _Optional[_Union[SeasonByYearValue, _Mapping]] = ...) -> None: ...

class SeasonByYearQuery(_message.Message):
    __slots__ = ("query_id", "year")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    year: int
    def __init__(self, query_id: _Optional[str] = ..., year: _Optional[int] = ...) -> None: ...
