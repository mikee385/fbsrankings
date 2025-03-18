from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SeasonByIDValue(_message.Message):
    __slots__ = ("season_id", "year")
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    season_id: str
    year: int
    def __init__(self, season_id: _Optional[str] = ..., year: _Optional[int] = ...) -> None: ...

class SeasonByIDResult(_message.Message):
    __slots__ = ("season",)
    SEASON_FIELD_NUMBER: _ClassVar[int]
    season: SeasonByIDValue
    def __init__(self, season: _Optional[_Union[SeasonByIDValue, _Mapping]] = ...) -> None: ...

class SeasonByIDQuery(_message.Message):
    __slots__ = ("query_id", "season_id")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    season_id: str
    def __init__(self, query_id: _Optional[str] = ..., season_id: _Optional[str] = ...) -> None: ...
