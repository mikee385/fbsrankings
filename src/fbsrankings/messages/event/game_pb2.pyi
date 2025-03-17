from google.protobuf import timestamp_pb2 as _timestamp_pb2
from fbsrankings.messages.enums import enums_pb2 as _enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GameCreatedEvent(_message.Message):
    __slots__ = ("event_id", "game_id", "season_id", "week", "date", "season_section", "home_team_id", "away_team_id", "notes")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    SEASON_SECTION_FIELD_NUMBER: _ClassVar[int]
    HOME_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    AWAY_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    game_id: str
    season_id: str
    week: int
    date: _timestamp_pb2.Timestamp
    season_section: _enums_pb2.SeasonSection
    home_team_id: str
    away_team_id: str
    notes: str
    def __init__(self, event_id: _Optional[str] = ..., game_id: _Optional[str] = ..., season_id: _Optional[str] = ..., week: _Optional[int] = ..., date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., season_section: _Optional[_Union[_enums_pb2.SeasonSection, str]] = ..., home_team_id: _Optional[str] = ..., away_team_id: _Optional[str] = ..., notes: _Optional[str] = ...) -> None: ...

class GameRescheduledEvent(_message.Message):
    __slots__ = ("event_id", "game_id", "season_id", "old_week", "old_date", "week", "date", "season_section", "home_team_id", "away_team_id", "notes")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    OLD_WEEK_FIELD_NUMBER: _ClassVar[int]
    OLD_DATE_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    SEASON_SECTION_FIELD_NUMBER: _ClassVar[int]
    HOME_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    AWAY_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    game_id: str
    season_id: str
    old_week: int
    old_date: _timestamp_pb2.Timestamp
    week: int
    date: _timestamp_pb2.Timestamp
    season_section: _enums_pb2.SeasonSection
    home_team_id: str
    away_team_id: str
    notes: str
    def __init__(self, event_id: _Optional[str] = ..., game_id: _Optional[str] = ..., season_id: _Optional[str] = ..., old_week: _Optional[int] = ..., old_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., week: _Optional[int] = ..., date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., season_section: _Optional[_Union[_enums_pb2.SeasonSection, str]] = ..., home_team_id: _Optional[str] = ..., away_team_id: _Optional[str] = ..., notes: _Optional[str] = ...) -> None: ...

class GameCanceledEvent(_message.Message):
    __slots__ = ("event_id", "game_id", "season_id", "week", "date", "season_section", "home_team_id", "away_team_id", "notes")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    SEASON_SECTION_FIELD_NUMBER: _ClassVar[int]
    HOME_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    AWAY_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    game_id: str
    season_id: str
    week: int
    date: _timestamp_pb2.Timestamp
    season_section: _enums_pb2.SeasonSection
    home_team_id: str
    away_team_id: str
    notes: str
    def __init__(self, event_id: _Optional[str] = ..., game_id: _Optional[str] = ..., season_id: _Optional[str] = ..., week: _Optional[int] = ..., date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., season_section: _Optional[_Union[_enums_pb2.SeasonSection, str]] = ..., home_team_id: _Optional[str] = ..., away_team_id: _Optional[str] = ..., notes: _Optional[str] = ...) -> None: ...

class GameCompletedEvent(_message.Message):
    __slots__ = ("event_id", "game_id", "season_id", "week", "date", "season_section", "home_team_id", "away_team_id", "home_team_score", "away_team_score", "notes")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    SEASON_SECTION_FIELD_NUMBER: _ClassVar[int]
    HOME_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    AWAY_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    HOME_TEAM_SCORE_FIELD_NUMBER: _ClassVar[int]
    AWAY_TEAM_SCORE_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    game_id: str
    season_id: str
    week: int
    date: _timestamp_pb2.Timestamp
    season_section: _enums_pb2.SeasonSection
    home_team_id: str
    away_team_id: str
    home_team_score: int
    away_team_score: int
    notes: str
    def __init__(self, event_id: _Optional[str] = ..., game_id: _Optional[str] = ..., season_id: _Optional[str] = ..., week: _Optional[int] = ..., date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., season_section: _Optional[_Union[_enums_pb2.SeasonSection, str]] = ..., home_team_id: _Optional[str] = ..., away_team_id: _Optional[str] = ..., home_team_score: _Optional[int] = ..., away_team_score: _Optional[int] = ..., notes: _Optional[str] = ...) -> None: ...

class GameNotesUpdatedEvent(_message.Message):
    __slots__ = ("event_id", "game_id", "season_id", "week", "date", "season_section", "home_team_id", "away_team_id", "old_notes", "notes")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    SEASON_SECTION_FIELD_NUMBER: _ClassVar[int]
    HOME_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    AWAY_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    OLD_NOTES_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    game_id: str
    season_id: str
    week: int
    date: _timestamp_pb2.Timestamp
    season_section: _enums_pb2.SeasonSection
    home_team_id: str
    away_team_id: str
    old_notes: str
    notes: str
    def __init__(self, event_id: _Optional[str] = ..., game_id: _Optional[str] = ..., season_id: _Optional[str] = ..., week: _Optional[int] = ..., date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., season_section: _Optional[_Union[_enums_pb2.SeasonSection, str]] = ..., home_team_id: _Optional[str] = ..., away_team_id: _Optional[str] = ..., old_notes: _Optional[str] = ..., notes: _Optional[str] = ...) -> None: ...
