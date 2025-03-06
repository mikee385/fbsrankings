from datetime import datetime
from typing import Optional
from uuid import UUID

from tinydb import Query

from communication.bus import EventBus
from fbsrankings.messages.event import GameRankingCalculatedEvent
from fbsrankings.messages.query import GameRankingBySeasonWeekQuery
from fbsrankings.messages.query import GameRankingBySeasonWeekResult
from fbsrankings.messages.query import GameRankingValueBySeasonWeekResult
from fbsrankings.storage.tinydb import Storage


class GameRankingBySeasonWeekQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._storage = storage
        self._event_bus = event_bus

        self._event_bus.register_handler(GameRankingCalculatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(GameRankingCalculatedEvent, self.project)

    def project(self, event: GameRankingCalculatedEvent) -> None:
        table = self._storage.connection.table("game_ranking_by_season_week")

        existing_season = self._storage.cache_season_by_id.get(str(event.season_id))
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found",
            )

        values = []
        for value in event.values:
            existing_game = self._storage.cache_game_by_id.get(str(value.id_))
            if existing_game is None:
                raise RuntimeError(
                    "Query database is out of sync with master database. "
                    f"Game {value.id_} was not found for game ranking {event.ranking_id}",
                )
            values.append(
                {
                    "id_": str(value.id_),
                    "season_id": existing_game["season_id"],
                    "year": existing_season["year"],
                    "week": existing_game["week"],
                    "date": existing_game["date"],
                    "season_section": existing_game["season_section"],
                    "home_team_id": existing_game["home_team_id"],
                    "home_team_name": existing_game["home_team_name"],
                    "away_team_id": existing_game["away_team_id"],
                    "away_team_name": existing_game["away_team_name"],
                    "home_team_score": existing_game["home_team_score"],
                    "away_team_score": existing_game["away_team_score"],
                    "status": existing_game["status"],
                    "notes": existing_game["notes"],
                    "order": value.order,
                    "rank": value.rank,
                    "value": value.value,
                },
            )

        existing = table.get(
            (Query().name == event.name)
            & (Query().season_id == str(event.season_id))
            & (Query().week == event.week),
        )
        if isinstance(existing, list):
            existing = existing[0]
        if existing is None:
            table.insert(
                {
                    "id_": str(event.ranking_id),
                    "name": event.name,
                    "season_id": str(event.season_id),
                    "year": existing_season["year"],
                    "week": event.week,
                    "values": values,
                },
            )

        elif existing["id_"] != str(event.ranking_id):
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"ID for game ranking does not match: "
                f"{existing['id_']} vs. {event.ranking_id}",
            )


class GameRankingBySeasonWeekQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(
        self,
        query: GameRankingBySeasonWeekQuery,
    ) -> Optional[GameRankingBySeasonWeekResult]:
        table = self._connection.table("game_ranking_by_season_week")

        item = table.get(
            (Query().name == query.name)
            & (Query().season_id == str(query.season_id))
            & (Query().week == query.week),
        )
        if isinstance(item, list):
            item = item[0]
        return (
            GameRankingBySeasonWeekResult(
                UUID(item["id_"]),
                item["name"],
                UUID(item["season_id"]),
                item["year"],
                item["week"],
                [
                    GameRankingValueBySeasonWeekResult(
                        UUID(value["id_"]),
                        UUID(value["season_id"]),
                        value["year"],
                        value["week"],
                        datetime.strptime(value["date"], "%Y-%m-%d").date(),
                        value["season_section"],
                        UUID(value["home_team_id"]),
                        value["home_team_name"],
                        UUID(value["away_team_id"]),
                        value["away_team_name"],
                        value["home_team_score"],
                        value["away_team_score"],
                        value["status"],
                        value["notes"],
                        value["order"],
                        value["rank"],
                        value["value"],
                    )
                    for value in item["values"]
                ],
            )
            if item is not None
            else None
        )
