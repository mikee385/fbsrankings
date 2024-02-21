from fbsrankings.domain import SeasonSection
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import PostseasonGameCountBySeasonQuery
from fbsrankings.query import PostseasonGameCountBySeasonResult


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
