from fbsrankings.messages.convert import date_to_timestamp
from fbsrankings.messages.enums import GameStatus
from fbsrankings.messages.query import CanceledGameResult
from fbsrankings.messages.query import CanceledGamesQuery
from fbsrankings.messages.query import CanceledGamesResult
from fbsrankings.storage.memory import Storage


class CanceledGamesQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: CanceledGamesQuery) -> CanceledGamesResult:
        games = []
        for game in self._storage.game.all_():
            if game.status == GameStatus.GAME_STATUS_CANCELED:
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
                            notes=game.notes,
                        ),
                    )

        return CanceledGamesResult(query_id=query.query_id, games=games)
