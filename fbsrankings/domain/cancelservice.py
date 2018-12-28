from fbsrankings.domain.season import Season, SeasonID, SeasonRepository
from fbsrankings.domain.game import GameStatus, GameRepository


class CancelService (object):
    def __init__(self, repository):
        if not isinstance(repository, SeasonRepository):
            raise TypeError('repository must be of type SeasonRepository')
        if not isinstance(repository, GameRepository):
            raise TypeError('repository must be of type GameRepository')
        self._repository = repository
        
    def cancel_past_games(self, year_or_season):
        if isinstance(year_or_season, Season) or isinstance(year_or_season, SeasonID):
            season = year_or_season
        elif isinstance(year_or_season, int):
            season = self._repository.find_season_by_year(year_or_season)
        else:
            raise TypeError('year_or_season must be of type Season, SeasonID, or int')
            
        if season is not None:
            games = self._repository.find_games_by_season(season)
            
            most_recent_completed_week = -1
            for game in games:
                if game.status == GameStatus.COMPLETED:
                    if game.week > most_recent_completed_week:
                        most_recent_completed_week = game.week
                        
            if most_recent_completed_week >= 0:
                for game in games:
                    if game.status == GameStatus.SCHEDULED and game.week < most_recent_completed_week:
                        game.cancel()
