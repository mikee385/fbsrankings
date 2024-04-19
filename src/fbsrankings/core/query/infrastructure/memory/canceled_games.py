from fbsrankings.core.query.query.canceled_games import CanceledGameResult
from fbsrankings.core.query.query.canceled_games import CanceledGamesQuery
from fbsrankings.core.query.query.canceled_games import CanceledGamesResult
from fbsrankings.enums import GameStatus
from fbsrankings.storage.memory import Storage


class CanceledGamesQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: CanceledGamesQuery) -> CanceledGamesResult:
        games = []
        for game in self._storage.game.all_():
            if game.status == GameStatus.CANCELED.name:
                season = self._storage.season.get(game.season_id)
                home_team = self._storage.team.get(game.home_team_id)
                away_team = self._storage.team.get(game.away_team_id)

                if (
                    season is not None
                    and home_team is not None
                    and away_team is not None
                ):
                    games.append(
                        CanceledGameResult(
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
                            game.notes,
                        ),
                    )

        return CanceledGamesResult(games)
