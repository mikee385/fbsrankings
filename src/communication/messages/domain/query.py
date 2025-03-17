from typing import Callable
from typing import Generic
from typing import Protocol
from typing import TypeVar


class QueryBase(Protocol):
    query_id: str


Q = TypeVar("Q", bound=QueryBase, contravariant=True)
R = TypeVar("R", covariant=True)


class Query(QueryBase, Generic[R], Protocol):
    pass


QueryHandler = Callable[[Q], R]
