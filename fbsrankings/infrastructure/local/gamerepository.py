from fbsrankings.domain import Season, SeasonID, SeasonSection, Team, TeamID, GameID, GameRepository as BaseRepository


class GameRepository(BaseRepository):
    def __init__(self):
        self._game_id_dict = {}
        self._game_season_dict = {}
        self._game_team_dict = {}
    
    def add(self, game):
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
