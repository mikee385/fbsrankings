"""Shared event classes for the fbsrankings package"""

from typing import Dict
from typing import Type

from fbsrankings.shared.messaging import Event

from .affiliation import AffiliationCreatedEvent
from .affiliation import AffiliationEventHandler
from .affiliation import AffiliationEventManager
from .game import GameCanceledEvent
from .game import GameCompletedEvent
from .game import GameCreatedEvent
from .game import GameEventHandler
from .game import GameEventManager
from .game import GameNotesUpdatedEvent
from .game import GameRescheduledEvent
from .ranking import GameRankingCalculatedEvent
from .ranking import GameRankingEventHandler
from .ranking import GameRankingEventManager
from .ranking import RankingCalculatedEvent
from .ranking import RankingValue
from .ranking import TeamRankingCalculatedEvent
from .ranking import TeamRankingEventHandler
from .ranking import TeamRankingEventManager
from .record import TeamRecordCalculatedEvent
from .record import TeamRecordEventHandler
from .record import TeamRecordEventManager
from .record import TeamRecordValue
from .season import SeasonCreatedEvent
from .season import SeasonEventHandler
from .season import SeasonEventManager
from .team import TeamCreatedEvent
from .team import TeamEventHandler
from .team import TeamEventManager


__all__ = [
    "AffiliationCreatedEvent",
    "AffiliationEventHandler",
    "AffiliationEventManager",
    "GameCanceledEvent",
    "GameCompletedEvent",
    "GameCreatedEvent",
    "GameEventHandler",
    "GameEventManager",
    "GameNotesUpdatedEvent",
    "GameRankingCalculatedEvent",
    "GameRankingEventHandler",
    "GameRankingEventManager",
    "GameRescheduledEvent",
    "RankingCalculatedEvent",
    "RankingValue",
    "SeasonCreatedEvent",
    "SeasonEventHandler",
    "SeasonEventManager",
    "TeamCreatedEvent",
    "TeamEventHandler",
    "TeamEventManager",
    "TeamRankingCalculatedEvent",
    "TeamRankingEventHandler",
    "TeamRankingEventManager",
    "TeamRecordCalculatedEvent",
    "TeamRecordEventHandler",
    "TeamRecordEventManager",
    "TeamRecordValue",
]

Topics: Dict[Type[Event], str] = {
    AffiliationCreatedEvent: "fbsrankings/event/affiliation_created",
    GameCanceledEvent: "fbsrankings/event/game_canceled",
    GameCompletedEvent: "fbsrankings/event/game_completed",
    GameCreatedEvent: "fbsrankings/event/game_created",
    GameNotesUpdatedEvent: "fbsrankings/event/game_notes_updated",
    GameRankingCalculatedEvent: "fbsrankings/event/game_ranking_calculated",
    GameRescheduledEvent: "fbsrankings/event/game_rescheduled",
    SeasonCreatedEvent: "fbsrankings/event/season_created",
    TeamCreatedEvent: "fbsrankings/event/team_created",
    TeamRankingCalculatedEvent: "fbsrankings/event/team_ranking_calculated",
    TeamRecordCalculatedEvent: "fbsrankings/event/team_record_calculated",
}
