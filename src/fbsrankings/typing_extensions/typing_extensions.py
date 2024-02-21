from typing import Any
from typing import TypeVar
from typing import Union

from typing_extensions import TypeAlias
from typing_extensions import Protocol


# Comparison protocols
# Copied from typeshed

_T_contra = TypeVar("_T_contra", contravariant=True)


class SupportsDunderLT(Protocol[_T_contra]):
    def __lt__(self, __other: _T_contra) -> bool:
        pass


class SupportsDunderGT(Protocol[_T_contra]):
    def __gt__(self, __other: _T_contra) -> bool:
        pass


SupportsRichComparison: TypeAlias = Union[SupportsDunderLT[Any], SupportsDunderGT[Any]]
