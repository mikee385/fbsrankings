from fbsrankings.domain import Season, SeasonID, SeasonSection, Team, TeamID, Game, GameRepository as BaseRepository, GameStatus
from fbsrankings.event import GameCreatedEvent, GameRescheduledEvent, GameCanceledEvent, GameCompletedEvent, GameNotesUpdatedEvent
from fbsrankings.infrastructure.memory.storage import GameStorage, GameDto
        

class GameRepository (BaseRepository):
    def __init__(self, storage, bus):
        super().__init__(bus)
        
        if not isinstance(storage, GameStorage):
            raise TypeError('storage must be of type GameStorage')
        self._storage = storage

    def get(self, ID):
        return self._to_game(self._storage.get(ID))
        
    def find(self, season, week, team1, team2):
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
            
        return self._to_game(self._storage.find(season_ID, week, team1_ID, team2_ID))
        
    def _to_game(self, dto):
        if dto is not None:
            return Game(self._bus, dto.ID, dto.season_ID, dto.week, dto.date, SeasonSection[dto.season_section], dto.home_team_ID, dto.away_team_ID, dto.home_team_score, dto.away_team_score, GameStatus[dto.status], dto.notes)
        return None
        
    def handle(self, event):
        if isinstance(event, GameCreatedEvent):
            self._handle_game_created(event)
            return True
        elif isinstance(event, GameRescheduledEvent):
            self._handle_game_rescheduled(event)
            return True
        elif isinstance(event, GameCanceledEvent):
            self._handle_game_canceled(event)
            return True
        elif isinstance(event, GameCompletedEvent):
            self._handle_game_completed(event)
            return True
        elif isinstance(event, GameNotesUpdatedEvent):
            self._handle_game_notes_updated(event)
            return True
        else:
            return False
        
    def _handle_game_created(self, event):
        self._storage.add(GameDto(event.ID, event.season_ID, event.week, event.date, event.season_section, event.home_team_ID, event.away_team_ID, None, None, GameStatus.SCHEDULED, event.notes))
        
    def _handle_game_rescheduled(self, event):
        dto = self._storage.get(event.ID)
        dto.week = event.week
        dto.date = event.date
    
    def _handle_game_canceled(self, event):
        dto = self._storage.get(event.ID)
        dto.status = GameStatus.CANCELED

    def _handle_game_completed(self, event):
        dto = self._storage.get(event.ID)
        dto.home_team_score = event.home_team_score
        dto.away_team_score = event.away_team_score
        dto.status = GameStatus.COMPLETED
    
    def _handle_game_notes_updated(self, event):
        dto = self._storage.get(event.ID)
        dto.notes = event.notes
