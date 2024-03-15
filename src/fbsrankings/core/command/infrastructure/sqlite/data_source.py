from fbsrankings.common import EventBus
from fbsrankings.core.command.infrastructure.event_handler import EventHandlerFactory
from fbsrankings.core.command.infrastructure.repository import RepositoryFactory
from fbsrankings.core.command.infrastructure.sqlite.event_handler import EventHandler
from fbsrankings.core.command.infrastructure.sqlite.repository import Repository
from fbsrankings.storage.sqlite import Storage


class DataSource(RepositoryFactory, EventHandlerFactory):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def repository(self, event_bus: EventBus) -> Repository:
        return Repository(self._storage, event_bus)

    def event_handler(self, event_bus: EventBus) -> EventHandler:
        return EventHandler(self._storage, event_bus)
