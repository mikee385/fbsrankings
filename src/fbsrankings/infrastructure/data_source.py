from abc import ABCMeta
from abc import abstractmethod
from types import TracebackType
from typing import ContextManager
from typing import Optional
from typing import Type

from typing_extensions import Literal

from fbsrankings.infrastructure.event_handler import EventHandlerFactory
from fbsrankings.infrastructure.query_manager import QueryManagerFactory
from fbsrankings.infrastructure.repository import RepositoryFactory


class DataSource(
    RepositoryFactory,
    EventHandlerFactory,
    QueryManagerFactory,
    ContextManager["DataSource"],
    metaclass=ABCMeta,
):
    @abstractmethod
    def drop(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self) -> "DataSource":
        raise NotImplementedError

    @abstractmethod
    def __exit__(
        self,
        type_: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        raise NotImplementedError
