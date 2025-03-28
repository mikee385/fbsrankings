from configparser import ConfigParser
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Literal
from typing import TypeVar
from typing import Union


E = TypeVar("E", bound=Enum)


class ChannelType(str, Enum):
    NONE = "none"
    MEMORY = "memory"


class SerializationType(str, Enum):
    NONE = "none"
    JSON = "json"
    PICKLE = "pickle"
    PROTOBUF = "protobuf"


class StorageType(str, Enum):
    MEMORY_SHARED = "memory-shared"
    SQLITE_SHARED = "sqlite-shared"
    SQLITE_TINYDB = "sqlite-tinydb"


SqliteFile = Union[Path, Literal[":memory:"]]


@dataclass(frozen=True)
class SqliteConfig:
    file: SqliteFile = Path("fbsrankings.db")

    def __post_init__(self) -> None:
        if not (isinstance(self.file, Path) or self.file == ":memory:"):
            raise ValueError(f"Invalid SQLite file: {self.file}")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SqliteConfig":
        file = data.get("file", "fbsrankings.db")
        if not isinstance(file, (str, Path)):
            raise ValueError(f"Invalid SQLite file value: {file}")
        if file == ":memory:":
            return cls(file=":memory:")
        return cls(file=Path(file))


TinyDbFile = Path


@dataclass(frozen=True)
class TinyDbConfig:
    file: TinyDbFile = Path("fbsrankings.json")

    def __post_init__(self) -> None:
        if not isinstance(self.file, Path):
            raise ValueError(f"Invalid TinyDB file path: {self.file}")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TinyDbConfig":
        file = data.get("file", "fbsrankings.json")
        if not isinstance(file, (str, Path)):
            raise ValueError(f"Invalid TinyDB file value: {file}")
        return cls(file=Path(file))


@dataclass(frozen=True)
class Config:
    channel: ChannelType
    serialization: SerializationType
    storage: StorageType

    alternate_names: dict[str, str] = field(default_factory=dict)

    sqlite: SqliteConfig = field(default_factory=SqliteConfig)
    tinydb: TinyDbConfig = field(default_factory=TinyDbConfig)

    def __post_init__(self) -> None:
        if not isinstance(self.channel, ChannelType):
            raise ValueError(f"Invalid channel type: {self.channel}")

        if not isinstance(self.serialization, SerializationType):
            raise ValueError(f"Invalid serialization type: {self.serialization}")

        if not isinstance(self.storage, StorageType):
            raise ValueError(f"Invalid storage type: {self.storage}")

        if not isinstance(self.alternate_names, dict) or not all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in self.alternate_names.items()
        ):
            raise ValueError(
                "alternate_names must be a dictionary with string keys and values",
            )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        def parse_enum(enum_cls: type[E], value: str) -> E:
            try:
                return enum_cls(value)
            except ValueError as ex:
                raise ValueError(
                    f"Invalid value '{value}' for {enum_cls.__name__}",
                ) from ex

        return cls(
            channel=parse_enum(
                ChannelType,
                data.get("channel", ChannelType.NONE.value),
            ),
            serialization=parse_enum(
                SerializationType,
                data.get("serialization", SerializationType.NONE.value),
            ),
            storage=parse_enum(
                StorageType,
                data.get("storage", StorageType.MEMORY_SHARED.value),
            ),
            alternate_names=data.get("alternate_names", {}),
            sqlite=SqliteConfig.from_dict(data.get("sqlite", {})),
            tinydb=TinyDbConfig.from_dict(data.get("tinydb", {})),
        )

    @classmethod
    def from_ini(cls, file_path: Path) -> "Config":
        data: dict[str, Any] = {}

        parser = ConfigParser()
        parser.read(file_path)

        if "fbsrankings" not in parser:
            raise ValueError(f"{file_path}: No [fbsrankings] section in config file")

        for key, value in parser["fbsrankings"].items():
            data[key] = value

        for header, section in parser.items():
            if header.startswith("fbsrankings."):
                name = header[12:]
                values = dict(section.items())
                data[name] = values

        return cls.from_dict(data)
