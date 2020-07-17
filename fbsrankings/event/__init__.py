"""Event classes for the fbsrankings package"""
from fbsrankings.event.affiliation import (
    AffiliationCreatedEvent as AffiliationCreatedEvent,
)
from fbsrankings.event.game import GameCanceledEvent as GameCanceledEvent
from fbsrankings.event.game import GameCompletedEvent as GameCompletedEvent
from fbsrankings.event.game import GameCreatedEvent as GameCreatedEvent
from fbsrankings.event.game import GameNotesUpdatedEvent as GameNotesUpdatedEvent
from fbsrankings.event.game import GameRescheduledEvent as GameRescheduledEvent
from fbsrankings.event.ranking import (
    GameRankingCalculatedEvent as GameRankingCalculatedEvent,
)
from fbsrankings.event.ranking import RankingCalculatedEvent as RankingCalculatedEvent
from fbsrankings.event.ranking import RankingValue as RankingValue
from fbsrankings.event.ranking import (
    TeamRankingCalculatedEvent as TeamRankingCalculatedEvent,
)
from fbsrankings.event.record import (
    TeamRecordCalculatedEvent as TeamRecordCalculatedEvent,
)
from fbsrankings.event.record import TeamRecordValue as TeamRecordValue
from fbsrankings.event.season import SeasonCreatedEvent as SeasonCreatedEvent
from fbsrankings.event.team import TeamCreatedEvent as TeamCreatedEvent
