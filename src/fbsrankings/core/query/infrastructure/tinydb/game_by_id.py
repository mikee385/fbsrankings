from datetime import datetime
from typing import Optional
from uuid import UUID

from fbsrankings.core.query.query.game_by_id import GameByIDQuery
from fbsrankings.core.query.query.game_by_id import GameByIDResult
from fbsrankings.storage.tinydb import Storage


class GameByIDQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: GameByIDQuery) -> Optional[GameByIDResult]:
        item = self._storage.cache_game_by_id.get(str(query.id_))

        return (
            GameByIDResult(
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
            if item is not None
            else None
        )
