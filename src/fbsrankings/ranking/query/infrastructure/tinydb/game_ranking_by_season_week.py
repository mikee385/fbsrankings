from datetime import datetime
from typing import Optional

from tinydb import Query

from communication.bus import EventBus
from fbsrankings.messages.convert import datetime_to_timestamp
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

        existing_season = self._storage.cache_season_by_id.get(event.season_id)
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found",
            )

        values = []
        for value in event.values:
            existing_game = self._storage.cache_game_by_id.get(value.id)
            if existing_game is None:
                raise RuntimeError(
                    "Query database is out of sync with master database. "
                    f"Game {value.id} was not found for game ranking {event.ranking_id}",
                )
            values.append(
                {
                    "id_": value.id,
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
            & (Query().season_id == event.season_id)
            & (Query().week == (event.week if event.HasField("week") else None)),
        )
        if isinstance(existing, list):
            existing = existing[0]
        if existing is None:
            table.insert(
                {
                    "id_": event.ranking_id,
                    "name": event.name,
                    "season_id": event.season_id,
                    "year": existing_season["year"],
                    "week": event.week if event.HasField("week") else None,
                    "values": values,
                },
            )

        elif existing["id_"] != event.ranking_id:
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
            & (Query().season_id == query.season_id)
            & (Query().week == (query.week if query.HasField("week") else None)),
        )
        if isinstance(item, list):
            item = item[0]
        return (
            GameRankingBySeasonWeekResult(
                ranking_id=item["id_"],
                name=item["name"],
                season_id=item["season_id"],
                year=item["year"],
                week=item["week"],
                values=[
                    GameRankingValueBySeasonWeekResult(
                        game_id=value["id_"],
                        season_id=value["season_id"],
                        year=value["year"],
                        week=value["week"],
                        date=datetime_to_timestamp(
                            datetime.strptime(value["date"], "%Y-%m-%d"),
                        ),
                        season_section=value["season_section"],
                        home_team_id=value["home_team_id"],
                        home_team_name=value["home_team_name"],
                        away_team_id=value["away_team_id"],
                        away_team_name=value["away_team_name"],
                        home_team_score=value["home_team_score"],
                        away_team_score=value["away_team_score"],
                        status=value["status"],
                        notes=value["notes"],
                        order=value["order"],
                        rank=value["rank"],
                        value=value["value"],
                    )
                    for value in item["values"]
                ],
            )
            if item is not None
            else None
        )
