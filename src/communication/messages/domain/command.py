from typing import Callable
from typing import Protocol
from typing import TypeVar


class Command(Protocol):
    command_id: str


C = TypeVar("C", bound=Command, contravariant=True)


CommandHandler = Callable[[C], None]
