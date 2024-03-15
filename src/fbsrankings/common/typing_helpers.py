# Utility types for typeshed
#
# Copied from typeshed on 2024-02-21:
# https://github.com/python/typeshed/blob/main/stdlib/_typeshed/__init__.pyi
from typing import Any
from typing import TypeVar
from typing import Union

from typing_extensions import Protocol

# Comparison protocols

_T_contra = TypeVar("_T_contra", contravariant=True)


class SupportsDunderLT(Protocol[_T_contra]):
    def __lt__(self, other: _T_contra) -> bool:
        ...


class SupportsDunderGT(Protocol[_T_contra]):
    def __gt__(self, other: _T_contra) -> bool:
        ...


SupportsRichComparison = Union[SupportsDunderLT[Any], SupportsDunderGT[Any]]
