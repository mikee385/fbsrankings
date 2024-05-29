from uuid import UUID

from dataclasses import dataclass

from fbsrankings.shared.messaging import Query


@dataclass(frozen=True)
class WeekCountBySeasonResult:
    season_id: UUID
    count: int


@dataclass(frozen=True)
class WeekCountBySeasonQuery(Query[WeekCountBySeasonResult]):
    season_id: UUID
