from fbsrankings.domain import Season, SeasonID, AffiliationRepository


class AffiliationQueryHandler (AffiliationRepository):
    def __init__(self, parent, repository):
        self._parent = parent
        
        if not isinstance(repository, AffiliationRepository):
            raise TypeError('repository must be of type AffiliationRepository')
        self._repository = repository
        
        super().__init__(self._repository._event_bus)
        
    def find_by_ID(self, ID):
        return self._repository.find_by_ID(ID)
        
    def find_by_season_team(self, season, team):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        self._parent._load_by_ID(season_ID)
        return self._repository.find_by_season_team(season, team)
        
    def find_by_season(self, season):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        self._parent._load_by_ID(season_ID)
        return self._repository.find_by_season(season)
