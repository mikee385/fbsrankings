"""Common message classes that can be utilized in any package"""

from .domain.command import C
from .domain.command import Command
from .domain.command import CommandHandler
from .domain.command import CommandTopicMapper
from .domain.error import Error
from .domain.error import MultipleError
from .domain.event import E
from .domain.event import Event
from .domain.event import EventHandler
from .domain.event import EventTopicMapper
from .domain.query import Q
from .domain.query import Query
from .domain.query import QueryHandler
from .domain.query import QueryTopicMapper
from .domain.query import R


__all__ = [
    "C",
    "Command",
    "CommandHandler",
    "CommandTopicMapper",
    "E",
    "Error",
    "Event",
    "EventHandler",
    "EventTopicMapper",
    "MultipleError",
    "Q",
    "Query",
    "QueryHandler",
    "QueryTopicMapper",
    "R",
]
