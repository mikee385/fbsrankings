from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AffiliationCountBySeasonResult(_message.Message):
    __slots__ = ("season_id", "fbs_count", "fcs_count")
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    FBS_COUNT_FIELD_NUMBER: _ClassVar[int]
    FCS_COUNT_FIELD_NUMBER: _ClassVar[int]
    season_id: str
    fbs_count: int
    fcs_count: int
    def __init__(self, season_id: _Optional[str] = ..., fbs_count: _Optional[int] = ..., fcs_count: _Optional[int] = ...) -> None: ...

class AffiliationCountBySeasonQuery(_message.Message):
    __slots__ = ("query_id", "season_id")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    season_id: str
    def __init__(self, query_id: _Optional[str] = ..., season_id: _Optional[str] = ...) -> None: ...
