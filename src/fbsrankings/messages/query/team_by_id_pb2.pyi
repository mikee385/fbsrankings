from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TeamByIDValue(_message.Message):
    __slots__ = ("team_id", "name")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    name: str
    def __init__(self, team_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class TeamByIDResult(_message.Message):
    __slots__ = ("query_id", "team")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    team: TeamByIDValue
    def __init__(self, query_id: _Optional[str] = ..., team: _Optional[_Union[TeamByIDValue, _Mapping]] = ...) -> None: ...

class TeamByIDQuery(_message.Message):
    __slots__ = ("query_id", "team_id")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    team_id: str
    def __init__(self, query_id: _Optional[str] = ..., team_id: _Optional[str] = ...) -> None: ...
