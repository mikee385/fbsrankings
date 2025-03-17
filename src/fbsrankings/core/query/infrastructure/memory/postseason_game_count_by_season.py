from fbsrankings.messages.enums import SeasonSection
from fbsrankings.messages.query import PostseasonGameCountBySeasonQuery
from fbsrankings.messages.query import PostseasonGameCountBySeasonResult
from fbsrankings.storage.memory import Storage


class PostseasonGameCountBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self,
        query: PostseasonGameCountBySeasonQuery,
    ) -> PostseasonGameCountBySeasonResult:
        return PostseasonGameCountBySeasonResult(
            season_id=query.season_id,
            count=sum(
                1
                for _ in filter(
                    lambda g: g.season_section
                    == SeasonSection.SEASON_SECTION_POSTSEASON,
                    self._storage.game.for_season(query.season_id),
                )
            ),
        )
