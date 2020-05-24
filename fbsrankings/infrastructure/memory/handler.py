from fbsrankings.common import EventBus
from fbsrankings.domain import Repository
from fbsrankings.infrastructure.memory import SeasonQueryHandler, TeamQueryHandler, AffiliationQueryHandler, GameQueryHandler


class QueryHandler (Repository):
    def __init__(self, data_source, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        
        super().__init__(
            SeasonQueryHandler(data_source.season, event_bus),
            TeamQueryHandler(data_source.team, event_bus),
            AffiliationQueryHandler(data_source.affiliation, event_bus),
            GameQueryHandler(data_source.game, event_bus)
        )
