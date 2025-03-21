from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SeasonResult(_message.Message):
    __slots__ = ("season_id", "year")
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    season_id: str
    year: int
    def __init__(self, season_id: _Optional[str] = ..., year: _Optional[int] = ...) -> None: ...

class SeasonsResult(_message.Message):
    __slots__ = ("query_id", "seasons")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    SEASONS_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    seasons: _containers.RepeatedCompositeFieldContainer[SeasonResult]
    def __init__(self, query_id: _Optional[str] = ..., seasons: _Optional[_Iterable[_Union[SeasonResult, _Mapping]]] = ...) -> None: ...

class SeasonsQuery(_message.Message):
    __slots__ = ("query_id",)
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    def __init__(self, query_id: _Optional[str] = ...) -> None: ...
