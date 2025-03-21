from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PostseasonGameCountBySeasonResult(_message.Message):
    __slots__ = ("query_id", "season_id", "count")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    season_id: str
    count: int
    def __init__(self, query_id: _Optional[str] = ..., season_id: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class PostseasonGameCountBySeasonQuery(_message.Message):
    __slots__ = ("query_id", "season_id")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    season_id: str
    def __init__(self, query_id: _Optional[str] = ..., season_id: _Optional[str] = ...) -> None: ...
