from typing import Optional

from dataclasses import dataclass

from communication.messages import Query


@dataclass(frozen=True)
class SeasonByIDResult:
    season_id: str
    year: int


@dataclass(frozen=True)
class SeasonByIDQuery(Query[Optional[SeasonByIDResult]]):
    query_id: str
    season_id: str
