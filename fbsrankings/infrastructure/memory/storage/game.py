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


class GameStorage (object):
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
