from fbsrankings.messages.convert import date_to_timestamp
from fbsrankings.messages.query import GameBySeasonResult
from fbsrankings.messages.query import GamesBySeasonQuery
from fbsrankings.messages.query import GamesBySeasonResult
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
                    ),
                )

        return GamesBySeasonResult(query_id=query.query_id, games=items)
