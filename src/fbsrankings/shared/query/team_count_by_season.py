from uuid import UUID

from dataclasses import dataclass

from fbsrankings.shared.messaging import Query


@dataclass(frozen=True)
class TeamCountBySeasonResult:
    season_id: UUID
    count: int


@dataclass(frozen=True)
class TeamCountBySeasonQuery(Query[TeamCountBySeasonResult]):
    season_id: UUID
