from fbsrankings.core.query.query.games_by_season import GameBySeasonResult
from fbsrankings.core.query.query.games_by_season import GamesBySeasonQuery
from fbsrankings.core.query.query.games_by_season import GamesBySeasonResult
from fbsrankings.storage.memory import Storage


class GamesBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: GamesBySeasonQuery) -> GamesBySeasonResult:
        season = self._storage.season.get(query.season_id)
        teams = {team.id_: team for team in self._storage.team.all_()}
        games = self._storage.game.for_season(query.season_id)

        items = []
        for game in games:
            home_team = teams.get(game.home_team_id)
            away_team = teams.get(game.away_team_id)

            if season is not None and home_team is not None and away_team is not None:
                items.append(
                    GameBySeasonResult(
                        game.id_,
                        game.season_id,
                        season.year,
                        game.week,
                        game.date,
                        game.season_section,
                        game.home_team_id,
                        home_team.name,
                        game.away_team_id,
                        away_team.name,
                        game.home_team_score,
                        game.away_team_score,
                        game.status,
                        game.notes,
                    ),
                )

        return GamesBySeasonResult(items)
