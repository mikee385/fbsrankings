from fbsrankings.messages.query import TeamRecordBySeasonWeekQuery
from fbsrankings.messages.query import TeamRecordBySeasonWeekResult
from fbsrankings.messages.query import TeamRecordBySeasonWeekValue
from fbsrankings.messages.query import TeamRecordValueBySeasonWeekResult
from fbsrankings.storage.memory import Storage


class TeamRecordBySeasonWeekQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self,
        query: TeamRecordBySeasonWeekQuery,
    ) -> TeamRecordBySeasonWeekResult:
        record = self._storage.team_record.find(
            query.season_id,
            query.week if query.HasField("week") else None,
        )
        if record is not None:
            season = self._storage.season.get(record.season_id)

            values = []
            for value in record.values:
                team = self._storage.team.get(value.team_id)
                if team is not None:
                    values.append(
                        TeamRecordValueBySeasonWeekResult(
                            team_id=value.team_id,
                            name=team.name,
                            wins=value.wins,
                            losses=value.losses,
                        ),
                    )

            if season is not None:
                return TeamRecordBySeasonWeekResult(
                    query_id=query.query_id,
                    record=TeamRecordBySeasonWeekValue(
                        record_id=str(record.id_),
                        season_id=str(record.season_id),
                        year=season.year,
                        week=record.week,
                        values=values,
                    ),
                )

        return TeamRecordBySeasonWeekResult(query_id=query.query_id, record=None)
