"""Common serialization classes that can be utilized in any package"""

from .domain.serializer import Serializer
from .infrastructure.pickle.serializer import PickleSerializer


__all__ = [
    "PickleSerializer",
    "Serializer",
]
