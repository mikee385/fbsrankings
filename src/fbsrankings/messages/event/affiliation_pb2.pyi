from fbsrankings.messages.enums import enums_pb2 as _enums_pb2
from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AffiliationCreatedEvent(_message.Message):
    __slots__ = ("event_id", "affiliation_id", "season_id", "team_id", "subdivision")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    AFFILIATION_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SUBDIVISION_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    affiliation_id: str
    season_id: str
    team_id: str
    subdivision: _enums_pb2.Subdivision
    def __init__(self, event_id: _Optional[str] = ..., affiliation_id: _Optional[str] = ..., season_id: _Optional[str] = ..., team_id: _Optional[str] = ..., subdivision: _Optional[_Union[_enums_pb2.Subdivision, str]] = ...) -> None: ...
