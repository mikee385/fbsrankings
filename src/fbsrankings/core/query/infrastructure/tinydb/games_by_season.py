from datetime import datetime
from uuid import UUID

from tinydb import Query

from fbsrankings.common import EventBus
from fbsrankings.core.command import GameCanceledEvent
from fbsrankings.core.command import GameCompletedEvent
from fbsrankings.core.command import GameCreatedEvent
from fbsrankings.core.command import GameNotesUpdatedEvent
from fbsrankings.core.command import GameRescheduledEvent
from fbsrankings.core.query.query.games_by_season import GameBySeasonResult
from fbsrankings.core.query.query.games_by_season import GamesBySeasonQuery
from fbsrankings.core.query.query.games_by_season import GamesBySeasonResult
from fbsrankings.enum import GameStatus
from fbsrankings.storage.tinydb import Storage


class GamesBySeasonQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._connection = storage.connection
        self._event_bus = event_bus

        self._event_bus.register_handler(GameCreatedEvent, self.project_created)
        self._event_bus.register_handler(GameCanceledEvent, self.project_canceled)
        self._event_bus.register_handler(GameCompletedEvent, self.project_completed)
        self._event_bus.register_handler(GameRescheduledEvent, self.project_rescheduled)
        self._event_bus.register_handler(
            GameNotesUpdatedEvent,
            self.project_notes_updated,
        )

    def close(self) -> None:
        self._event_bus.unregister_handler(GameCreatedEvent, self.project_created)
        self._event_bus.unregister_handler(GameCanceledEvent, self.project_canceled)
        self._event_bus.unregister_handler(GameCompletedEvent, self.project_completed)
        self._event_bus.unregister_handler(
            GameRescheduledEvent,
            self.project_rescheduled,
        )
        self._event_bus.unregister_handler(
            GameNotesUpdatedEvent,
            self.project_notes_updated,
        )

    def project_created(self, event: GameCreatedEvent) -> None:
        table = self._connection.table("games")

        season_table = self._connection.table("seasons")
        existing_season = season_table.get(Query().id_ == str(event.season_id))
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found for game {event.id_}",
            )

        team_table = self._connection.table("teams")
        existing_home_team = team_table.get(Query().id_ == str(event.home_team_id))
        if existing_home_team is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Home Team {event.home_team_id} was not found for game {event.id_}",
            )
        existing_away_team = team_table.get(Query().id_ == str(event.away_team_id))
        if existing_away_team is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Home Team {event.away_team_id} was not found for game {event.id_}",
            )

        if event.home_team_id < event.away_team_id:
            team1_id = event.home_team_id
            team2_id = event.away_team_id
        else:
            team1_id = event.away_team_id
            team2_id = event.home_team_id

        existing = table.get(
            (Query().season_id == str(event.season_id))
            & (Query().week == event.week)
            & (Query().team1_id == str(team1_id))
            & (Query().team2_id == str(team2_id)),
        )
        if existing is None:
            table.insert(
                {
                    "id_": str(event.id_),
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "week": event.week,
                    "date": event.date.strftime("%Y-%m-%d"),
                    "season_section": event.season_section,
                    "home_team_id": str(event.home_team_id),
                    "home_team_name": existing_home_team["name"],
                    "away_team_id": str(event.away_team_id),
                    "away_team_name": existing_away_team["name"],
                    "home_team_score": None,
                    "away_team_score": None,
                    "status": GameStatus.SCHEDULED.name,
                    "notes": event.notes,
                },
            )

        elif existing["id_"] != str(event.id_):
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for game does not match: "
                f"{existing['id_']} vs. {event.id_}",
            )

    def project_canceled(self, event: GameCanceledEvent) -> None:
        table = self._connection.table("games")

        existing = table.update(
            {"status": GameStatus.CANCELED.name},
            Query().id_ == str(event.id_),
        )

        if len(existing) == 0:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
            )

    def project_completed(self, event: GameCompletedEvent) -> None:
        table = self._connection.table("games")

        existing = table.update(
            {
                "home_team_score": event.home_team_score,
                "away_team_score": event.away_team_score,
                "status": GameStatus.COMPLETED.name,
            },
            Query().id_ == str(event.id_),
        )

        if len(existing) == 0:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
            )

    def project_rescheduled(self, event: GameRescheduledEvent) -> None:
        table = self._connection.table("games")

        existing = table.update(
            {"week": event.week, "date": event.date.strftime("%Y-%m-%d")},
            Query().id_ == str(event.id_),
        )

        if len(existing) == 0:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
            )

    def project_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        table = self._connection.table("games")

        existing = table.update({"notes": event.notes}, Query().id_ == str(event.id_))

        if len(existing) == 0:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
            )


class GamesBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(self, query: GamesBySeasonQuery) -> GamesBySeasonResult:
        table = self._connection.table("games")

        items = [
            GameBySeasonResult(
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
                item["home_team_score"],
                item["away_team_score"],
                item["status"],
                item["notes"],
            )
            for item in table.search(Query().season_id == str(query.season_id))
        ]

        return GamesBySeasonResult(items)
