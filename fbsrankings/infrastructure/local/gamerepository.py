from fbsrankings.domain.game import GameID, GameRepository as BaseRepository
from fbsrankings.domain.season import Season, SeasonID


class GameRepository(BaseRepository):
    def __init__(self):
        self._game_id_dict = {}
        self._game_season_dict = {}
    
    def add_game(self, game):
        self._game_id_dict[game.ID] = game
        
        season_dict = self._game_season_dict.get(game.season_ID)
        if season_dict is None:
            season_dict = {}
            self._game_season_dict[game.season_ID] = season_dict
        season_dict[game.ID] = game

    def find_game(self, ID):
        if not isinstance(ID, GameID):
            raise TypeError('ID must be of type GameID')
        return self._game_id_dict.get(ID)
        
    def find_games_by_season(self, season):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        season_dict = self._game_season_dict.get(season_ID)
        if season_dict is None:
            return None
        return list(season_dict.values())
        
    def all_games(self):
        return self._game_id_dict.values()
