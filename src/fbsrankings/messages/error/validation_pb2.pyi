from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SeasonDataValidationError(_message.Message):
    __slots__ = ("event_id", "message", "season_id", "attribute_name", "attribute_value", "expected_value")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_VALUE_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    message: str
    season_id: str
    attribute_name: str
    attribute_value: str
    expected_value: str
    def __init__(self, event_id: _Optional[str] = ..., message: _Optional[str] = ..., season_id: _Optional[str] = ..., attribute_name: _Optional[str] = ..., attribute_value: _Optional[str] = ..., expected_value: _Optional[str] = ...) -> None: ...

class TeamDataValidationError(_message.Message):
    __slots__ = ("event_id", "message", "team_id", "attribute_name", "attribute_value", "expected_value")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_VALUE_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    message: str
    team_id: str
    attribute_name: str
    attribute_value: str
    expected_value: str
    def __init__(self, event_id: _Optional[str] = ..., message: _Optional[str] = ..., team_id: _Optional[str] = ..., attribute_name: _Optional[str] = ..., attribute_value: _Optional[str] = ..., expected_value: _Optional[str] = ...) -> None: ...

class AffiliationDataValidationError(_message.Message):
    __slots__ = ("event_id", "message", "affiliation_id", "attribute_name", "attribute_value", "expected_value")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    AFFILIATION_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_VALUE_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    message: str
    affiliation_id: str
    attribute_name: str
    attribute_value: str
    expected_value: str
    def __init__(self, event_id: _Optional[str] = ..., message: _Optional[str] = ..., affiliation_id: _Optional[str] = ..., attribute_name: _Optional[str] = ..., attribute_value: _Optional[str] = ..., expected_value: _Optional[str] = ...) -> None: ...

class GameDataValidationError(_message.Message):
    __slots__ = ("event_id", "message", "game_id", "attribute_name", "attribute_value", "expected_value")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    GAME_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_VALUE_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    message: str
    game_id: str
    attribute_name: str
    attribute_value: str
    expected_value: str
    def __init__(self, event_id: _Optional[str] = ..., message: _Optional[str] = ..., game_id: _Optional[str] = ..., attribute_name: _Optional[str] = ..., attribute_value: _Optional[str] = ..., expected_value: _Optional[str] = ...) -> None: ...

class FBSGameCountValidationError(_message.Message):
    __slots__ = ("event_id", "message", "season_id", "team_id", "game_count")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    message: str
    season_id: str
    team_id: str
    game_count: int
    def __init__(self, event_id: _Optional[str] = ..., message: _Optional[str] = ..., season_id: _Optional[str] = ..., team_id: _Optional[str] = ..., game_count: _Optional[int] = ...) -> None: ...

class FCSGameCountValidationError(_message.Message):
    __slots__ = ("event_id", "message", "season_id", "team_id", "game_count")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    message: str
    season_id: str
    team_id: str
    game_count: int
    def __init__(self, event_id: _Optional[str] = ..., message: _Optional[str] = ..., season_id: _Optional[str] = ..., team_id: _Optional[str] = ..., game_count: _Optional[int] = ...) -> None: ...

class PostseasonGameCountValidationError(_message.Message):
    __slots__ = ("event_id", "message", "season_id", "regular_season_game_count", "postseason_game_count")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    REGULAR_SEASON_GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    POSTSEASON_GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    message: str
    season_id: str
    regular_season_game_count: int
    postseason_game_count: int
    def __init__(self, event_id: _Optional[str] = ..., message: _Optional[str] = ..., season_id: _Optional[str] = ..., regular_season_game_count: _Optional[int] = ..., postseason_game_count: _Optional[int] = ...) -> None: ...
