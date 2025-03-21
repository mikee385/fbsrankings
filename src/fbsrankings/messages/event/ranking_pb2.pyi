from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RankingValue(_message.Message):
    __slots__ = ("id", "order", "rank", "value")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    id: str
    order: int
    rank: int
    value: float
    def __init__(self, id: _Optional[str] = ..., order: _Optional[int] = ..., rank: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...

class TeamRankingCalculatedEvent(_message.Message):
    __slots__ = ("event_id", "ranking_id", "name", "season_id", "week", "values")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    RANKING_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    ranking_id: str
    name: str
    season_id: str
    week: int
    values: _containers.RepeatedCompositeFieldContainer[RankingValue]
    def __init__(self, event_id: _Optional[str] = ..., ranking_id: _Optional[str] = ..., name: _Optional[str] = ..., season_id: _Optional[str] = ..., week: _Optional[int] = ..., values: _Optional[_Iterable[_Union[RankingValue, _Mapping]]] = ...) -> None: ...

class GameRankingCalculatedEvent(_message.Message):
    __slots__ = ("event_id", "ranking_id", "name", "season_id", "week", "values")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    RANKING_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    ranking_id: str
    name: str
    season_id: str
    week: int
    values: _containers.RepeatedCompositeFieldContainer[RankingValue]
    def __init__(self, event_id: _Optional[str] = ..., ranking_id: _Optional[str] = ..., name: _Optional[str] = ..., season_id: _Optional[str] = ..., week: _Optional[int] = ..., values: _Optional[_Iterable[_Union[RankingValue, _Mapping]]] = ...) -> None: ...
