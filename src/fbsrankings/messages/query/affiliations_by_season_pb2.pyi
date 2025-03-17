from fbsrankings.messages.enums import enums_pb2 as _enums_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AffiliationBySeasonResult(_message.Message):
    __slots__ = ("affiliation_id", "season_id", "year", "team_id", "team_name", "subdivision")
    AFFILIATION_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    SUBDIVISION_FIELD_NUMBER: _ClassVar[int]
    affiliation_id: str
    season_id: str
    year: int
    team_id: str
    team_name: str
    subdivision: _enums_pb2.Subdivision
    def __init__(self, affiliation_id: _Optional[str] = ..., season_id: _Optional[str] = ..., year: _Optional[int] = ..., team_id: _Optional[str] = ..., team_name: _Optional[str] = ..., subdivision: _Optional[_Union[_enums_pb2.Subdivision, str]] = ...) -> None: ...

class AffiliationsBySeasonResult(_message.Message):
    __slots__ = ("affiliations",)
    AFFILIATIONS_FIELD_NUMBER: _ClassVar[int]
    affiliations: _containers.RepeatedCompositeFieldContainer[AffiliationBySeasonResult]
    def __init__(self, affiliations: _Optional[_Iterable[_Union[AffiliationBySeasonResult, _Mapping]]] = ...) -> None: ...

class AffiliationsBySeasonQuery(_message.Message):
    __slots__ = ("query_id", "season_id")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    season_id: str
    def __init__(self, query_id: _Optional[str] = ..., season_id: _Optional[str] = ...) -> None: ...
