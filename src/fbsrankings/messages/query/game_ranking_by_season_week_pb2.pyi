from google.protobuf import timestamp_pb2 as _timestamp_pb2
from fbsrankings.messages.enums import enums_pb2 as _enums_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GameRankingValueBySeasonWeekResult(_message.Message):
    __slots__ = ("game_id", "season_id", "year", "week", "date", "season_section", "home_team_id", "home_team_name", "away_team_id", "away_team_name", "home_team_score", "away_team_score", "status", "notes", "order", "rank", "value")
    GAME_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    SEASON_SECTION_FIELD_NUMBER: _ClassVar[int]
    HOME_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    HOME_TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    AWAY_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    AWAY_TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    HOME_TEAM_SCORE_FIELD_NUMBER: _ClassVar[int]
    AWAY_TEAM_SCORE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    game_id: str
    season_id: str
    year: int
    week: int
    date: _timestamp_pb2.Timestamp
    season_section: _enums_pb2.SeasonSection
    home_team_id: str
    home_team_name: str
    away_team_id: str
    away_team_name: str
    home_team_score: int
    away_team_score: int
    status: _enums_pb2.GameStatus
    notes: str
    order: int
    rank: int
    value: float
    def __init__(self, game_id: _Optional[str] = ..., season_id: _Optional[str] = ..., year: _Optional[int] = ..., week: _Optional[int] = ..., date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., season_section: _Optional[_Union[_enums_pb2.SeasonSection, str]] = ..., home_team_id: _Optional[str] = ..., home_team_name: _Optional[str] = ..., away_team_id: _Optional[str] = ..., away_team_name: _Optional[str] = ..., home_team_score: _Optional[int] = ..., away_team_score: _Optional[int] = ..., status: _Optional[_Union[_enums_pb2.GameStatus, str]] = ..., notes: _Optional[str] = ..., order: _Optional[int] = ..., rank: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...

class GameRankingBySeasonWeekValue(_message.Message):
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
    values: _containers.RepeatedCompositeFieldContainer[GameRankingValueBySeasonWeekResult]
    def __init__(self, ranking_id: _Optional[str] = ..., name: _Optional[str] = ..., season_id: _Optional[str] = ..., year: _Optional[int] = ..., week: _Optional[int] = ..., values: _Optional[_Iterable[_Union[GameRankingValueBySeasonWeekResult, _Mapping]]] = ...) -> None: ...

class GameRankingBySeasonWeekResult(_message.Message):
    __slots__ = ("ranking",)
    RANKING_FIELD_NUMBER: _ClassVar[int]
    ranking: GameRankingBySeasonWeekValue
    def __init__(self, ranking: _Optional[_Union[GameRankingBySeasonWeekValue, _Mapping]] = ...) -> None: ...

class GameRankingBySeasonWeekQuery(_message.Message):
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
