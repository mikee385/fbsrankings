from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TeamRecordValue(_message.Message):
    __slots__ = ("team_id", "wins", "losses", "games", "win_percentage")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    WINS_FIELD_NUMBER: _ClassVar[int]
    LOSSES_FIELD_NUMBER: _ClassVar[int]
    GAMES_FIELD_NUMBER: _ClassVar[int]
    WIN_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    wins: int
    losses: int
    games: int
    win_percentage: float
    def __init__(self, team_id: _Optional[str] = ..., wins: _Optional[int] = ..., losses: _Optional[int] = ..., games: _Optional[int] = ..., win_percentage: _Optional[float] = ...) -> None: ...

class TeamRecordCalculatedEvent(_message.Message):
    __slots__ = ("event_id", "record_id", "season_id", "week", "values")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    RECORD_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    record_id: str
    season_id: str
    week: int
    values: _containers.RepeatedCompositeFieldContainer[TeamRecordValue]
    def __init__(self, event_id: _Optional[str] = ..., record_id: _Optional[str] = ..., season_id: _Optional[str] = ..., week: _Optional[int] = ..., values: _Optional[_Iterable[_Union[TeamRecordValue, _Mapping]]] = ...) -> None: ...
