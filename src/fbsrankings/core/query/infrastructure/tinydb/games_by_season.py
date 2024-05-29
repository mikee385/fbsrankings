from datetime import datetime
from uuid import UUID

from tinydb import Query
from tinydb.table import Document

from fbsrankings.shared.enums import GameStatus
from fbsrankings.shared.event import GameCanceledEvent
from fbsrankings.shared.event import GameCompletedEvent
from fbsrankings.shared.event import GameCreatedEvent
from fbsrankings.shared.event import GameNotesUpdatedEvent
from fbsrankings.shared.event import GameRescheduledEvent
from fbsrankings.shared.messaging import EventBus
from fbsrankings.shared.query import GameBySeasonResult
from fbsrankings.shared.query import GamesBySeasonQuery
from fbsrankings.shared.query import GamesBySeasonResult
from fbsrankings.storage.tinydb import Storage


class GamesBySeasonQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._storage = storage
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
        existing_season = self._storage.cache_season_by_id.get(str(event.season_id))
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found for game {event.id_}",
            )

        existing_home_team = self._storage.cache_team_by_id.get(str(event.home_team_id))
        if existing_home_team is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Home Team {event.home_team_id} was not found for game {event.id_}",
            )

        existing_away_team = self._storage.cache_team_by_id.get(str(event.away_team_id))
        if existing_away_team is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Away Team {event.away_team_id} was not found for game {event.id_}",
            )

        item = {
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
        }

        existing_by_id = self._storage.cache_game_by_id.get(str(event.id_))
        if existing_by_id is not None and (
            existing_by_id["season_id"] != item["season_id"]
            or existing_by_id["week"] != item["week"]
            or existing_by_id["home_team_id"] != item["home_team_id"]
            or existing_by_id["away_team_id"] != item["away_team_id"]
        ):
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Data for game {event.id_} does not match: "
                f"{existing_by_id['season_id']} vs. {item['season_id']}, ",
                f"{existing_by_id['week']} vs. {item['week']}, ",
                f"{existing_by_id['home_team_id']} vs. {item['home_team_id']}, ",
                f"{existing_by_id['away_team_id']} vs. {item['away_team_id']}",
            )

        doc_id = self._storage.connection.table("games").insert(item)
        document = Document(item, doc_id)
        self._storage.cache_game_by_id[str(event.id_)] = document

    def project_canceled(self, event: GameCanceledEvent) -> None:
        existing_by_id = self._storage.cache_game_by_id.get(str(event.id_))
        if existing_by_id is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
            )

        existing = self._storage.connection.table("games").update(
            {"status": GameStatus.CANCELED.name},
            Query().id_ == str(event.id_),
        )

        if len(existing) == 0:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
            )

        existing_by_id["status"] = GameStatus.CANCELED.name

    def project_completed(self, event: GameCompletedEvent) -> None:
        existing_by_id = self._storage.cache_game_by_id.get(str(event.id_))
        if existing_by_id is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
            )

        existing = self._storage.connection.table("games").update(
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

        existing_by_id["home_team_score"] = event.home_team_score
        existing_by_id["away_team_score"] = event.away_team_score
        existing_by_id["status"] = GameStatus.COMPLETED.name

    def project_rescheduled(self, event: GameRescheduledEvent) -> None:
        existing_by_id = self._storage.cache_game_by_id.get(str(event.id_))
        if existing_by_id is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
            )

        existing = self._storage.connection.table("games").update(
            {"week": event.week, "date": event.date.strftime("%Y-%m-%d")},
            Query().id_ == str(event.id_),
        )

        if len(existing) == 0:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
            )

        existing_by_id["week"] = event.week
        existing_by_id["date"] = event.date.strftime("%Y-%m-%d")

    def project_notes_updated(self, event: GameNotesUpdatedEvent) -> None:
        existing_by_id = self._storage.cache_game_by_id.get(str(event.id_))
        if existing_by_id is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
            )

        existing = self._storage.connection.table("games").update(
            {"notes": event.notes},
            Query().id_ == str(event.id_),
        )

        if len(existing) == 0:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Game {event.id_} was not found",
            )

        existing_by_id["notes"] = event.notes


class GamesBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: GamesBySeasonQuery) -> GamesBySeasonResult:
        return GamesBySeasonResult(
            [
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
                for item in self._storage.cache_game_by_id.values()
                if item["season_id"] == str(query.season_id)
            ],
        )
