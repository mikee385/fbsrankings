from typing import Any
from typing import TypeVar
from typing import Union

from typing_extensions import TypeAlias
from typing_extensions import Protocol


# Comparison protocols
# Copied from typeshed

T = TypeVar("T", contravariant=True)


class SupportsDunderLT(Protocol[T]):
    def __lt__(self, other: T) -> bool:
        raise NotImplementedError


class SupportsDunderGT(Protocol[T]):
    def __gt__(self, other: T) -> bool:
        raise NotImplementedError


SupportsRichComparison: TypeAlias = Union[SupportsDunderLT[Any], SupportsDunderGT[Any]]
