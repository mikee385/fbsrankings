from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TeamRecordValueBySeasonWeekResult(_message.Message):
    __slots__ = ("team_id", "name", "wins", "losses")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WINS_FIELD_NUMBER: _ClassVar[int]
    LOSSES_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    name: str
    wins: int
    losses: int
    def __init__(self, team_id: _Optional[str] = ..., name: _Optional[str] = ..., wins: _Optional[int] = ..., losses: _Optional[int] = ...) -> None: ...

class TeamRecordBySeasonWeekValue(_message.Message):
    __slots__ = ("record_id", "season_id", "year", "week", "values")
    RECORD_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    record_id: str
    season_id: str
    year: int
    week: int
    values: _containers.RepeatedCompositeFieldContainer[TeamRecordValueBySeasonWeekResult]
    def __init__(self, record_id: _Optional[str] = ..., season_id: _Optional[str] = ..., year: _Optional[int] = ..., week: _Optional[int] = ..., values: _Optional[_Iterable[_Union[TeamRecordValueBySeasonWeekResult, _Mapping]]] = ...) -> None: ...

class TeamRecordBySeasonWeekResult(_message.Message):
    __slots__ = ("query_id", "record")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    RECORD_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    record: TeamRecordBySeasonWeekValue
    def __init__(self, query_id: _Optional[str] = ..., record: _Optional[_Union[TeamRecordBySeasonWeekValue, _Mapping]] = ...) -> None: ...

class TeamRecordBySeasonWeekQuery(_message.Message):
    __slots__ = ("query_id", "season_id", "week")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    season_id: str
    week: int
    def __init__(self, query_id: _Optional[str] = ..., season_id: _Optional[str] = ..., week: _Optional[int] = ...) -> None: ...
