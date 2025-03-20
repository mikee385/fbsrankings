from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TeamRankingValueBySeasonWeekResult(_message.Message):
    __slots__ = ("team_id", "name", "order", "rank", "value")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    name: str
    order: int
    rank: int
    value: float
    def __init__(self, team_id: _Optional[str] = ..., name: _Optional[str] = ..., order: _Optional[int] = ..., rank: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...

class TeamRankingBySeasonWeekValue(_message.Message):
    __slots__ = ("ranking_id", "name", "season_id", "year", "week", "values")
    RANKING_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    ranking_id: str
    name: str
    season_id: str
    year: int
    week: int
    values: _containers.RepeatedCompositeFieldContainer[TeamRankingValueBySeasonWeekResult]
    def __init__(self, ranking_id: _Optional[str] = ..., name: _Optional[str] = ..., season_id: _Optional[str] = ..., year: _Optional[int] = ..., week: _Optional[int] = ..., values: _Optional[_Iterable[_Union[TeamRankingValueBySeasonWeekResult, _Mapping]]] = ...) -> None: ...

class TeamRankingBySeasonWeekResult(_message.Message):
    __slots__ = ("ranking",)
    RANKING_FIELD_NUMBER: _ClassVar[int]
    ranking: TeamRankingBySeasonWeekValue
    def __init__(self, ranking: _Optional[_Union[TeamRankingBySeasonWeekValue, _Mapping]] = ...) -> None: ...

class TeamRankingBySeasonWeekQuery(_message.Message):
    __slots__ = ("query_id", "name", "season_id", "week")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    name: str
    season_id: str
    week: int
    def __init__(self, query_id: _Optional[str] = ..., name: _Optional[str] = ..., season_id: _Optional[str] = ..., week: _Optional[int] = ...) -> None: ...
