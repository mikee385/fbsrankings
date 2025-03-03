"""Classes for connecting Channels to Buses"""

from .domain.command import CommandBridge
from .domain.event import EventBridge


__all__ = [
    "CommandBridge",
    "EventBridge",
]
