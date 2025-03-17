"""Event message classes for the fbsrankings package"""

from communication.messages import Event

from .affiliation_pb2 import AffiliationCreatedEvent
from .game_pb2 import GameCanceledEvent
from .game_pb2 import GameCompletedEvent
from .game_pb2 import GameCreatedEvent
from .game_pb2 import GameNotesUpdatedEvent
from .game_pb2 import GameRescheduledEvent
from .ranking_pb2 import GameRankingCalculatedEvent
from .ranking_pb2 import RankingValue
from .ranking_pb2 import TeamRankingCalculatedEvent
from .record_pb2 import TeamRecordCalculatedEvent
from .record_pb2 import TeamRecordValue
from .season_pb2 import SeasonCreatedEvent
from .team_pb2 import TeamCreatedEvent


__all__ = [
    "AffiliationCreatedEvent",
    "GameCanceledEvent",
    "GameCompletedEvent",
    "GameCreatedEvent",
    "GameNotesUpdatedEvent",
    "GameRankingCalculatedEvent",
    "GameRescheduledEvent",
    "RankingValue",
    "SeasonCreatedEvent",
    "TeamCreatedEvent",
    "TeamRankingCalculatedEvent",
    "TeamRecordCalculatedEvent",
    "TeamRecordValue",
]

Topics: dict[type[Event], str] = {
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
