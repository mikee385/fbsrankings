from fbsrankings.core.command.infrastructure.event_handler import EventHandlerFactory
from fbsrankings.core.command.infrastructure.memory.event_handler import EventHandler
from fbsrankings.core.command.infrastructure.memory.repository import Repository
from fbsrankings.core.command.infrastructure.repository import RepositoryFactory
from fbsrankings.shared.messaging import EventBus
from fbsrankings.storage.memory import Storage


class DataSource(RepositoryFactory, EventHandlerFactory):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def repository(self, event_bus: EventBus) -> Repository:
        return Repository(self._storage, event_bus)

    def event_handler(self, event_bus: EventBus) -> EventHandler:
        return EventHandler(self._storage, event_bus)
