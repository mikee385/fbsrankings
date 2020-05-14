from fbsrankings.common import EventBus
from fbsrankings.domain import Season, SeasonID, Team, TeamID, Game, GameRepository as BaseRepository, GameStatus
from fbsrankings.event import GameScheduledEvent, GameRescheduledEvent, GameCanceledEvent, GameCompletedEvent, GameNotesUpdatedEvent


class GameDto (object):
    def __init__(self, ID, season_ID, week, date_, season_section, home_team_ID, away_team_ID, home_team_score, away_team_score, status, notes):
        self.ID = ID
        self.season_ID = season_ID
        self.week = week
        self.date = date_
        self.season_section = season_section
        self.home_team_ID = home_team_ID
        self.away_team_ID = away_team_ID
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.status = status
        self.notes = notes


class GameDataStore (object):
    def __init__(self):
        self._game_id_dict = {}
        self._game_season_dict = {}
        self._game_team_dict = {}
    
    def add(self, game):
        if not isinstance(game, GameDto):
            raise TypeError('game must be of type GameDto')
            
        key = self._get_key(game.season_ID, game.week, game.home_team_ID, game.away_team_ID)
        if key in self._game_team_dict:
            raise ValueError(f'Game already exists for week {game.week} in season {game.season_ID} between {game.home_team_ID} and {game.away_team_ID}')
        self._game_team_dict[key] = game
        
        self._game_id_dict[game.ID] = game
        
        season_dict = self._game_season_dict.get(game.season_ID)
        if season_dict is None:
            season_dict = {}
            self._game_season_dict[game.season_ID] = season_dict
        season_dict[game.ID] = game

    def find_by_ID(self, ID):
        return self._game_id_dict.get(ID)

    def find_by_season_teams(self, season_ID, week, team1_ID, team2_ID):
        key = self._get_key(season_ID, week, team1_ID, team2_ID)
        return self._game_team_dict.get(key)
        
    def find_by_season(self, season_ID):
        season_dict = self._game_season_dict.get(season_ID)
        if season_dict is None:
            return []
        return [item for item in season_dict.values()]
        
    def all(self):
        return [item for item in self._game_id_dict.values()]
        
    def _get_key(self, season_ID, week, team1_ID, team2_ID):
        if team1_ID < team2_ID:
            return (season_ID, week, team1_ID, team2_ID)
        else:
            return (season_ID, week, team2_ID, team1_ID)
        

class GameRepository (BaseRepository):
    def __init__(self, data_store, event_bus):
        if not isinstance(data_store, GameDataStore):
            raise TypeError('data_store must be of type GameDataStore')
        self._data_store = data_store
        
        if not isinstance(event_bus, EventBus):
            raise TypeError('event_bus must be of type EventBus')
        self._event_bus = event_bus
        
    def _to_game(self, dto):
        if dto is not None:
            return Game(self._event_bus, dto.ID, dto.season_ID, dto.week, dto.date, dto.season_section, dto.home_team_ID, dto.away_team_ID, dto.home_team_score, dto.away_team_score, dto.status, dto.notes)
        return None

    def find_by_ID(self, ID):
        return self._to_game(self._data_store.find_by_ID(ID))
        
    def find_by_season_teams(self, season, week, team1, team2):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
        
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
            
        return self._to_game(self._data_store.find_by_season_teams(season_ID, week, team1_ID, team2_ID))
        
    def find_by_season(self, season):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')

        return [self._to_game(item) for item in self._data_store.find_by_season(season_ID)]
        
    def all(self):
        return [self._to_game(item) for item in self._data_store.all()]
        
    def try_handle_event(self, event):
        if isinstance(event, GameScheduledEvent):
            self._data_store.add(GameDto(event.ID, event.season_ID, event.week, event.date, event.season_section, event.home_team_ID, event.away_team_ID, None, None, GameStatus.SCHEDULED, event.notes))
            return True
        elif isinstance(event, GameRescheduledEvent):
            dto = self._data_store.find_by_ID(event.ID)
            dto.week = event.week
            dto.date = event.date
            return True
        elif isinstance(event, GameCanceledEvent):
            dto = self._data_store.find_by_ID(event.ID)
            dto.status = GameStatus.CANCELED
            return True
        elif isinstance(event, GameCompletedEvent):
            dto = self._data_store.find_by_ID(event.ID)
            dto.home_team_score = event.home_team_score
            dto.away_team_score = event.away_team_score
            dto.status = GameStatus.COMPLETED
            return True
        elif isinstance(event, GameNotesUpdatedEvent):
            dto = self._data_store.find_by_ID(event.ID)
            dto.notes = event.notes
            return True
        else:
            return False
