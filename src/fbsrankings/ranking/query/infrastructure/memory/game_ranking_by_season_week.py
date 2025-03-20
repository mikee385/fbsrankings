from fbsrankings.messages.convert import date_to_timestamp
from fbsrankings.messages.query import GameRankingBySeasonWeekQuery
from fbsrankings.messages.query import GameRankingBySeasonWeekResult
from fbsrankings.messages.query import GameRankingBySeasonWeekValue
from fbsrankings.messages.query import GameRankingValueBySeasonWeekResult
from fbsrankings.storage.memory import Storage


class GameRankingBySeasonWeekQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(
        self,
        query: GameRankingBySeasonWeekQuery,
    ) -> GameRankingBySeasonWeekResult:
        ranking = self._storage.game_ranking.find(
            query.name,
            query.season_id,
            query.week if query.HasField("week") else None,
        )
        if ranking is not None:
            season = self._storage.season.get(ranking.season_id)
            if season is not None:
                values = []
                for value in ranking.values:
                    game = self._storage.game.get(value.id_)

                    if game is not None:
                        home_team = self._storage.team.get(game.home_team_id)
                        away_team = self._storage.team.get(game.away_team_id)

                        if home_team is not None and away_team is not None:
                            values.append(
                                GameRankingValueBySeasonWeekResult(
                                    game_id=str(game.id_),
                                    season_id=str(game.season_id),
                                    year=season.year,
                                    week=game.week,
                                    date=date_to_timestamp(game.date),
                                    season_section=game.season_section,
                                    home_team_id=str(game.home_team_id),
                                    home_team_name=home_team.name,
                                    away_team_id=str(game.away_team_id),
                                    away_team_name=away_team.name,
                                    home_team_score=game.home_team_score,
                                    away_team_score=game.away_team_score,
                                    status=game.status,
                                    notes=game.notes,
                                    order=value.order,
                                    rank=value.rank,
                                    value=value.value,
                                ),
                            )

                return GameRankingBySeasonWeekResult(
                    query_id=query.query_id,
                    ranking=GameRankingBySeasonWeekValue(
                        ranking_id=str(ranking.id_),
                        name=ranking.name,
                        season_id=str(ranking.season_id),
                        year=season.year,
                        week=ranking.week,
                        values=values,
                    ),
                )

        return GameRankingBySeasonWeekResult(query_id=query.query_id, ranking=None)
