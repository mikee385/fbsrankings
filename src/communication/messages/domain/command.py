from typing import Callable
from typing import Optional
from typing import Protocol
from typing import TypeVar


class Command(Protocol):
    command_id: str


C = TypeVar("C", bound=Command, contravariant=True)


CommandHandler = Callable[[C], None]


class CommandTopicMapper(Protocol):
    def get(self, key: type[C]) -> Optional[str]:
        raise NotImplementedError
