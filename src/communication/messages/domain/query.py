from typing import Callable
from typing import Generic
from typing import TypeVar

from typing_extensions import Protocol


class QueryBase(Protocol):
    query_id: str


Q = TypeVar("Q", bound=QueryBase, contravariant=True)
R = TypeVar("R", covariant=True)


class Query(QueryBase, Generic[R], Protocol):
    pass


QueryHandler = Callable[[Q], R]
