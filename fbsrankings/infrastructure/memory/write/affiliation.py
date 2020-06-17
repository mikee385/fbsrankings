from fbsrankings.domain import Season, SeasonID, Team, TeamID, Affiliation, AffiliationRepository as BaseRepository
from fbsrankings.event import AffiliationRegisteredEvent
from fbsrankings.infrastructure.memory.storage import AffiliationStorage, AffiliationDto


class AffiliationRepository (BaseRepository):
    def __init__(self, storage, bus):
        super().__init__(bus)
        
        if not isinstance(storage, AffiliationStorage):
            raise TypeError('storage must be of type AffiliationDataSource')
        self._storage = storage
        
    def _to_affiliation(self, dto):
        if dto is not None:
            return Affiliation(self._bus, dto.ID, dto.season_ID, dto.team_ID, dto.subdivision)
        return None

    def find_by_ID(self, ID):
        return self._to_affiliation(self._storage.find_by_ID(ID))
        
    def find_by_season_team(self, season, team):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        if isinstance(team, Team):
            team_ID = team.ID
        elif isinstance(team, TeamID):
            team_ID = team
        else:
            raise TypeError('team must be of type Team or TeamID')
            
        return self._to_affiliation(self._storage.find_by_season_team(season_ID, team_ID))
        
    def find_by_season(self, season):
        if isinstance(season, Season):
            season_ID = season.ID
        elif isinstance(season, SeasonID):
            season_ID = season
        else:
            raise TypeError('season must be of type Season or SeasonID')
            
        return [self._to_affiliation(item) for item in self._storage.find_by_season(season_ID)]
        
    def handle(self, event):
        if isinstance(event, AffiliationRegisteredEvent):
            self._handle_affiliation_registered(event)
            return True
        else:
            return False
        
    def _handle_affiliation_registered(self, event):
        self._storage.add(AffiliationDto(event.ID, event.season_ID, event.team_ID, event.subdivision))
