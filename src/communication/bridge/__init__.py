"""Classes for connecting Channels to Buses"""

from .domain.command import CommandBridge
from .domain.event import EventBridge
from .domain.query import QueryBridge


__all__ = [
    "CommandBridge",
    "EventBridge",
    "QueryBridge",
]
