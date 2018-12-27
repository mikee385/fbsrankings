from uuid import uuid4

from fbsrankings.common.event import EventBus
from fbsrankings.domain.game import Game, GameID, GameRepository as BaseRepository
from fbsrankings.domain.season import Season, SeasonID


class GameRepository(BaseRepository):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self._game_id_dict = {}
        self._game_season_dict = {}
    
    def add_game(self, *args, **kwargs):
        ID = GameID(uuid4())
        value = Game(self._event_bus, ID, *args, **kwargs)
        
        self._game_id_dict[ID] = value
        
        season_dict = self._game_season_dict.get(value.season_ID)
        if season_dict is None:
            season_dict = {}
            self._game_season_dict[value.season_ID] = season_dict
        season_dict[value.ID] = value
        
        return value

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
