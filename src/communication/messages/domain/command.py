from typing import Callable
from typing import TypeVar
from uuid import UUID

from typing_extensions import Protocol


class Command(Protocol):
    command_id: UUID


C = TypeVar("C", bound=Command, contravariant=True)


CommandHandler = Callable[[C], None]
