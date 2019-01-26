from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID, SeasonSection, Team, TeamID, Game, GameID, GameRepository as BaseRepository, GameStatus, GameScheduledEvent, GameRescheduledEvent, GameCanceledEvent, GameCompletedEvent


class GameDataStore (BaseRepository):
    def __init__(self, event_bus):
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
        self._game_id_dict = {}
        self._game_season_dict = {}
        self._game_team_dict = {}
    
    def add(self, game):
        if not isinstance(game, Game):
            raise TypeError('game must be of type Game')
            
        game = game.copy(self._event_bus)
        
        self._game_id_dict[game.ID] = game
        
        season_dict = self._game_season_dict.get(game.season_ID)
        if season_dict is None:
            season_dict = {}
            self._game_season_dict[game.season_ID] = season_dict
        season_dict[game.ID] = game
        
        key = self._get_key(game.season_ID, game.season_section, game.week, game.home_team_ID, game.away_team_ID)
        self._game_team_dict[key] = game

    def find_by_ID(self, ID):
        if not isinstance(ID, GameID):
            raise TypeError('ID must be of type GameID')
        return self._game_id_dict.get(ID)

    def find_by_season_teams(self, season, season_section, week, team1, team2):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        if not isinstance(season_section, SeasonSection):
            raise TypeError('season_section must be of type SeasonSection')
        
        if isinstance(team1, Team):
            team1_ID = team1.ID
        elif isinstance(team1, TeamID):
            team1_ID = team1
        else:
            raise TypeError('team1 must be of type Team or TeamID')
            
        if isinstance(team2, Team):
            team2_ID = team2.ID
        elif isinstance(team2, TeamID):
            team2_ID = team2
        else:
            raise TypeError('team2 must be of type Team or TeamID')
            
        key = self._get_key(season_ID, season_section, week, team1_ID, team2_ID)
        return self._game_team_dict.get(key)
        
    def find_by_season(self, season):
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
        
    def all(self):
        return self._game_id_dict.values()
        
    def _get_key(self, season_ID, season_section, week, team1_ID, team2_ID):
        if team1_ID < team2_ID:
            return (season_ID, season_section, week, team1_ID, team2_ID)
        else:
            return (season_ID, season_section, week, team2_ID, team1_ID)
        

class GameRepository (BaseRepository):
    def __init__(self, data_store, event_bus):
        if not isinstance(data_store, GameDataStore):
            raise TypeError('data_store must be of type GameDataStore')
        self._data_store = data_store
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
    def add(self, game):
        # Handled through events
        pass

    def find_by_ID(self, ID):
        return self._copy(self._data_store.find_by_ID(ID))
        
    def find_by_season_teams(self, season, season_section, week, team1, team2):
        return self._copy(self._data_store.find_by_season_teams(season, season_section, week, team1, team2))
        
    def find_by_season(self, season):
        return [self._copy(item) for item in self._data_store.find_by_season(season)]
        
    def all(self):
        return [self._copy(item) for item in self._data_store.all()]
        
    def _copy(self, item):
        return item.copy(self._event_bus) if item is not None else None
        
    def try_handle_event(self, event):
        if isinstance(event, GameScheduledEvent):
            self._data_store.add(Game(self._event_bus, event.ID, event.season_ID, event.week, event.date, event.season_section, event.home_team_ID, event.away_team_ID, None, None, GameStatus.SCHEDULED, event.notes))
            return True
        elif isinstance(event, GameRescheduledEvent):
            game = self._data_store.find_by_ID(event.ID)
            game.reschedule(event.week, event.date_)
            return True
        elif isinstance(event, GameCanceledEvent):
            game = self._data_store.find_by_ID(event.ID)
            game.cancel()
            return True
        elif isinstance(event, GameCompletedEvent):
            game = self._data_store.find_by_ID(event.ID)
            game.complete(event.home_team_score, event.away_team_score)
            return True
        else:
            return False
