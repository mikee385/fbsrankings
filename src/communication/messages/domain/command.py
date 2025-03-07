from typing import Callable
from typing import TypeVar

from typing_extensions import Protocol


class Command(Protocol):
    command_id: str


C = TypeVar("C", bound=Command, contravariant=True)


CommandHandler = Callable[[C], None]
