from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class Subdivision(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUBDIVISION_UNSPECIFIED: _ClassVar[Subdivision]
    SUBDIVISION_FBS: _ClassVar[Subdivision]
    SUBDIVISION_FCS: _ClassVar[Subdivision]

class SeasonSection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEASON_SECTION_UNSPECIFIED: _ClassVar[SeasonSection]
    SEASON_SECTION_REGULAR_SEASON: _ClassVar[SeasonSection]
    SEASON_SECTION_POSTSEASON: _ClassVar[SeasonSection]

class GameStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GAME_STATUS_UNSPECIFIED: _ClassVar[GameStatus]
    GAME_STATUS_SCHEDULED: _ClassVar[GameStatus]
    GAME_STATUS_COMPLETED: _ClassVar[GameStatus]
    GAME_STATUS_CANCELED: _ClassVar[GameStatus]
SUBDIVISION_UNSPECIFIED: Subdivision
SUBDIVISION_FBS: Subdivision
SUBDIVISION_FCS: Subdivision
SEASON_SECTION_UNSPECIFIED: SeasonSection
SEASON_SECTION_REGULAR_SEASON: SeasonSection
SEASON_SECTION_POSTSEASON: SeasonSection
GAME_STATUS_UNSPECIFIED: GameStatus
GAME_STATUS_SCHEDULED: GameStatus
GAME_STATUS_COMPLETED: GameStatus
GAME_STATUS_CANCELED: GameStatus
