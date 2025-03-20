from tinydb import Query

from communication.bus import EventBus
from fbsrankings.messages.event import TeamRankingCalculatedEvent
from fbsrankings.messages.query import TeamRankingBySeasonWeekQuery
from fbsrankings.messages.query import TeamRankingBySeasonWeekResult
from fbsrankings.messages.query import TeamRankingBySeasonWeekValue
from fbsrankings.messages.query import TeamRankingValueBySeasonWeekResult
from fbsrankings.storage.tinydb import Storage


class TeamRankingBySeasonWeekQueryProjection:
    def __init__(self, storage: Storage, event_bus: EventBus) -> None:
        self._storage = storage
        self._event_bus = event_bus

        self._event_bus.register_handler(TeamRankingCalculatedEvent, self.project)

    def close(self) -> None:
        self._event_bus.unregister_handler(TeamRankingCalculatedEvent, self.project)

    def project(self, event: TeamRankingCalculatedEvent) -> None:
        table = self._storage.connection.table("team_ranking_by_season_week")

        existing_season = self._storage.cache_season_by_id.get(event.season_id)
        if existing_season is None:
            raise RuntimeError(
                "Query database is out of sync with master database. "
                f"Season {event.season_id} was not found",
            )

        values = []
        for value in event.values:
            existing_team = self._storage.cache_team_by_id.get(value.id)
            if existing_team is None:
                raise RuntimeError(
                    "Query database is out of sync with master database. "
                    f"Team {value.id} was not found for team ranking {event.ranking_id}",
                )
            values.append(
                {
                    "id_": value.id,
                    "name": existing_team["name"],
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
                f"ID for team ranking does not match: "
                f"{existing['id_']} vs. {event.ranking_id}",
            )


class TeamRankingBySeasonWeekQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._connection = storage.connection

    def __call__(
        self,
        query: TeamRankingBySeasonWeekQuery,
    ) -> TeamRankingBySeasonWeekResult:
        table = self._connection.table("team_ranking_by_season_week")

        item = table.get(
            (Query().name == query.name)
            & (Query().season_id == query.season_id)
            & (Query().week == (query.week if query.HasField("week") else None)),
        )
        if isinstance(item, list):
            item = item[0]

        if item is not None:
            return TeamRankingBySeasonWeekResult(
                ranking=TeamRankingBySeasonWeekValue(
                    ranking_id=item["id_"],
                    name=item["name"],
                    season_id=item["season_id"],
                    year=item["year"],
                    week=item["week"],
                    values=[
                        TeamRankingValueBySeasonWeekResult(
                            team_id=value["id_"],
                            name=value["name"],
                            order=value["order"],
                            rank=value["rank"],
                            value=value["value"],
                        )
                        for value in item["values"]
                    ],
                ),
            )

        return TeamRankingBySeasonWeekResult(ranking=None)
