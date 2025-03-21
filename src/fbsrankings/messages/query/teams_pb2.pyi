from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TeamResult(_message.Message):
    __slots__ = ("team_id", "name")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    name: str
    def __init__(self, team_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class TeamsResult(_message.Message):
    __slots__ = ("query_id", "teams")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    teams: _containers.RepeatedCompositeFieldContainer[TeamResult]
    def __init__(self, query_id: _Optional[str] = ..., teams: _Optional[_Iterable[_Union[TeamResult, _Mapping]]] = ...) -> None: ...

class TeamsQuery(_message.Message):
    __slots__ = ("query_id",)
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    def __init__(self, query_id: _Optional[str] = ...) -> None: ...
