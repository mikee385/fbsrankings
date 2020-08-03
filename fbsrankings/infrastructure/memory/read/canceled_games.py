from fbsrankings.domain import GameStatus
from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import CanceledGameResult
from fbsrankings.query import CanceledGamesQuery
from fbsrankings.query import CanceledGamesResult


class CanceledGamesQueryHandler(object):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: CanceledGamesQuery) -> CanceledGamesResult:
        games = []
        for game in self._storage.game.all():
            if game.status == GameStatus.CANCELED.name:
                season = self._storage.season.get(game.season_ID)
                home_team = self._storage.team.get(game.home_team_ID)
                away_team = self._storage.team.get(game.away_team_ID)

                if (
                    season is not None
                    and home_team is not None
                    and away_team is not None
                ):
                    games.append(
                        CanceledGameResult(
                            game.ID,
                            game.season_ID,
                            season.year,
                            game.week,
                            game.date,
                            game.season_section,
                            game.home_team_ID,
                            home_team.name,
                            game.away_team_ID,
                            away_team.name,
                            game.notes,
                        ),
                    )

        return CanceledGamesResult(games)
