from fbsrankings.core.query.query.postseason_game_count_by_season import (
    PostseasonGameCountBySeasonQuery,
)
from fbsrankings.core.query.query.postseason_game_count_by_season import (
    PostseasonGameCountBySeasonResult,
)
from fbsrankings.enum import SeasonSection
from fbsrankings.storage.memory import Storage


class PostseasonGameCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self,
        query: PostseasonGameCountBySeasonQuery,
    ) -> PostseasonGameCountBySeasonResult:
        return PostseasonGameCountBySeasonResult(
            query.season_id,
            sum(
                1
                for _ in filter(
                    lambda g: g.season_section == SeasonSection.POSTSEASON.name,
                    self._storage.game.for_season(query.season_id),
                )
            ),
        )
