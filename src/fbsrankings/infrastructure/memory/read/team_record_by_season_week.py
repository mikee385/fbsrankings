from typing import Optional

from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import TeamRecordBySeasonWeekQuery
from fbsrankings.query import TeamRecordBySeasonWeekResult
from fbsrankings.query import TeamRecordValueBySeasonWeekResult


class TeamRecordBySeasonWeekQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self, query: TeamRecordBySeasonWeekQuery,
    ) -> Optional[TeamRecordBySeasonWeekResult]:
        record = self._storage.team_record.find(query.season_id, query.week)
        if record is not None:
            season = self._storage.season.get(record.season_id)

            values = []
            for value in record.values:
                team = self._storage.team.get(value.team_id)
                if team is not None:
                    values.append(
                        TeamRecordValueBySeasonWeekResult(
                            value.team_id, team.name, value.wins, value.losses,
                        ),
                    )

            if season is not None:
                return TeamRecordBySeasonWeekResult(
                    record.id_, record.season_id, season.year, record.week, values,
                )
        return None
