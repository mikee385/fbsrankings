import sqlite3

from fbsrankings.common import EventBus
from fbsrankings.domain import Repository as BaseRepository
from fbsrankings.infrastructure.sqlite import SeasonRepository, TeamRepository, AffiliationRepository, GameRepository


class Repository (BaseRepository):
    def __init__(self, connection, event_bus):
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError('connection must be of type sqlite3.Connection')
        
        super().__init__(SeasonRepository(connection, event_bus), TeamRepository(connection, event_bus), AffiliationRepository(connection, event_bus), GameRepository(connection, event_bus))
