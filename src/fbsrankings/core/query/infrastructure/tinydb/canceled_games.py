from datetime import datetime
from uuid import UUID

from tinydb import Query

from fbsrankings.common import EventBus
from fbsrankings.core.command import GameCanceledEvent
from fbsrankings.core.command import GameNotesUpdatedEvent
from fbsrankings.core.query.query.canceled_games import CanceledGameResult
from fbsrankings.core.query.query.canceled_games import CanceledGamesQuery
from fbsrankings.core.query.query.canceled_games import CanceledGamesResult
from fbsrankings.storage.tinydb import Storage


class CanceledGamesQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._connection = storage.connection
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
        table = self._connection.table("canceled_games")

        season_table = self._connection.table("seasons")
        existing_season = season_table.get(Query().id_ == str(event.season_id))
        if isinstance(existing_season, list):
            existing_season = existing_season[0]
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found for game {event.id_}",
            )

        team_table = self._connection.table("teams")
        existing_home_team = team_table.get(Query().id_ == str(event.home_team_id))
        if isinstance(existing_home_team, list):
            existing_home_team = existing_home_team[0]
        if existing_home_team is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Home Team {event.home_team_id} was not found for game {event.id_}",
            )
        existing_away_team = team_table.get(Query().id_ == str(event.away_team_id))
        if isinstance(existing_away_team, list):
            existing_away_team = existing_away_team[0]
        if existing_away_team is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Away Team {event.away_team_id} was not found for game {event.id_}",
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
                    "notes": event.notes,
                },
            )

        elif existing["id_"] != str(event.id_):
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for game does not match: "
                f"{existing['id_']} vs. {event.id_}",
            )

    def project_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        table = self._connection.table("games")

        existing = table.update({"notes": event.notes}, Query().id_ == str(event.id_))

        if len(existing) == 0:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
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
