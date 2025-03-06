from datetime import datetime
from uuid import UUID

from tinydb import Query

from communication.bus import EventBus
from fbsrankings.messages.event import GameCanceledEvent
from fbsrankings.messages.event import GameNotesUpdatedEvent
from fbsrankings.messages.query import CanceledGameResult
from fbsrankings.messages.query import CanceledGamesQuery
from fbsrankings.messages.query import CanceledGamesResult
from fbsrankings.storage.tinydb import Storage


class CanceledGamesQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._storage = storage
        self._event_bus = event_bus

        self._event_bus.register_handler(GameCanceledEvent, self.project_canceled)
        self._event_bus.register_handler(
            GameNotesUpdatedEvent,
            self.project_notes_updated,
        )

    def close(self) -> None:
        self._event_bus.unregister_handler(GameCanceledEvent, self.project_canceled)
        self._event_bus.unregister_handler(
            GameNotesUpdatedEvent,
            self.project_notes_updated,
        )

    def project_canceled(self, event: GameCanceledEvent) -> None:
        table = self._storage.connection.table("canceled_games")

        existing_season = self._storage.cache_season_by_id.get(str(event.season_id))
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found for game {event.game_id}",
            )

        existing_home_team = self._storage.cache_team_by_id.get(str(event.home_team_id))
        if existing_home_team is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Home Team {event.home_team_id} was not found for game {event.game_id}",
            )
        existing_away_team = self._storage.cache_team_by_id.get(str(event.away_team_id))
        if existing_away_team is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Away Team {event.away_team_id} was not found for game {event.game_id}",
            )

        if event.home_team_id < event.away_team_id:
            team1_id = event.home_team_id
            team2_id = event.away_team_id
        else:
            team1_id = event.away_team_id
            team2_id = event.home_team_id

        existing = table.get(
            (Query().season_id == event.season_id)
            & (Query().week == event.week)
            & (Query().team1_id == team1_id)
            & (Query().team2_id == team2_id),
        )
        if isinstance(existing, list):
            existing = existing[0]
        if existing is None:
            table.insert(
                {
                    "id_": str(event.game_id),
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "week": event.week,
                    "date": event.date.strftime("%Y-%m-%d"),
                    "season_section": event.season_section,
                    "home_team_id": str(event.home_team_id),
                    "home_team_name": existing_home_team["name"],
                    "away_team_id": str(event.away_team_id),
                    "away_team_name": existing_away_team["name"],
                    "notes": event.notes,
                },
            )

        elif existing["id_"] != str(event.game_id):
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for game does not match: "
                f"{existing['id_']} vs. {event.game_id}",
            )

    def project_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        table = self._storage.connection.table("canceled_games")

        existing = table.update(
            {"notes": event.notes},
            Query().id_ == str(event.game_id),
        )

        if len(existing) == 0:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.game_id} was not found",
            )


class CanceledGamesQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(self, query: CanceledGamesQuery) -> CanceledGamesResult:
        table = self._connection.table("canceled_games")

        items = [
            CanceledGameResult(
                UUID(item["id_"]),
                UUID(item["season_id"]),
                item["year"],
                item["week"],
                datetime.strptime(item["date"], "%Y-%m-%d").date(),
                item["season_section"],
                UUID(item["home_team_id"]),
                item["home_team_name"],
                UUID(item["away_team_id"]),
                item["away_team_name"],
                item["notes"],
            )
            for item in table.all()
        ]

        return CanceledGamesResult(items)
