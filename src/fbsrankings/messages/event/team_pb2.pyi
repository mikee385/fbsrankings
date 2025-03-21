from fbsrankings.messages.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TeamCreatedEvent(_message.Message):
    __slots__ = ("event_id", "team_id", "name")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    team_id: str
    name: str
    def __init__(self, event_id: _Optional[str] = ..., team_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
