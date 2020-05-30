from fbsrankings.domain import Season, SeasonID, GameRepository


class GameQueryHandler (GameRepository):
    def __init__(self, parent, repository):
        self._parent = parent
        
        if not isinstance(repository, GameRepository):
            raise TypeError('repository must be of type GameRepository')
        self._repository = repository
    
    def find_by_ID(self, ID):
        return self._repository.find_by_ID(ID)
        
    def find_by_season_teams(self, season, week, team1, team2):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        self._parent._load_by_ID(season_ID)
        return self._repository.find_by_season_teams(season, week, team1, team2)
        
    def find_by_season(self, season):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        self._parent._load_by_ID(season_ID)
        return self._repository.find_by_season(season)
        
    def all(self):
        self._parent.load_all()
        return self._repository.all()
