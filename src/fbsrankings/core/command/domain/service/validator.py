import datetime
from typing import Iterable
from typing import Optional
from uuid import uuid4

from communication.bus import EventBus
from fbsrankings.core.command.domain.model.affiliation import Affiliation
from fbsrankings.core.command.domain.model.game import Game
from fbsrankings.core.command.domain.model.season import Season
from fbsrankings.core.command.domain.model.season import SeasonID
from fbsrankings.core.command.domain.model.team import Team
from fbsrankings.core.command.domain.model.team import TeamID
from fbsrankings.messages.enums import GameStatus
from fbsrankings.messages.enums import SeasonSection
from fbsrankings.messages.enums import Subdivision
from fbsrankings.messages.error import AffiliationDataValidationError
from fbsrankings.messages.error import FBSGameCountValidationError
from fbsrankings.messages.error import FCSGameCountValidationError
from fbsrankings.messages.error import GameDataValidationError
from fbsrankings.messages.error import PostseasonGameCountValidationError
from fbsrankings.messages.error import SeasonDataValidationError
from fbsrankings.messages.error import TeamDataValidationError


class Validator:
    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def validate_season_data(self, season: Season, year: int) -> None:
        if season.year != year:
            self._event_bus.publish(
                SeasonDataValidationError(
                    str(uuid4()),
                    f"Season.year does not match year: {season.year} vs. {year}",
                    str(season.id_),
                    "year",
                    season.year,
                    year,
                ),
            )

    def validate_team_data(self, team: Team, name: str) -> None:
        if team.name != name:
            self._event_bus.publish(
                TeamDataValidationError(
                    str(uuid4()),
                    f"Team.name does not match name: {team.name} vs. {name}",
                    str(team.id_),
                    "name",
                    team.name,
                    name,
                ),
            )

    def validate_affiliation_data(
        self,
        affiliation: Affiliation,
        season_id: SeasonID,
        team_id: TeamID,
        subdivision: Subdivision,
    ) -> None:
        if affiliation.season_id != season_id:
            self._event_bus.publish(
                AffiliationDataValidationError(
                    str(uuid4()),
                    "Affiliation.season_id does not match season_id:"
                    f" {affiliation.season_id} vs. {season_id}",
                    str(affiliation.id_),
                    "season_id",
                    str(affiliation.season_id),
                    str(season_id),
                ),
            )
        if affiliation.team_id != team_id:
            self._event_bus.publish(
                AffiliationDataValidationError(
                    str(uuid4()),
                    "Affiliation.team_id does not match team_id:"
                    f" {affiliation.team_id} vs. {team_id}",
                    str(affiliation.id_),
                    "team_id",
                    str(affiliation.team_id),
                    str(team_id),
                ),
            )
        if affiliation.subdivision != subdivision:
            self._event_bus.publish(
                AffiliationDataValidationError(
                    str(uuid4()),
                    "Affiliation.subdivision does not match subdivision:"
                    f" {affiliation.subdivision} vs. {subdivision}",
                    str(affiliation.id_),
                    "subdivision",
                    affiliation.subdivision.name,
                    subdivision.name,
                ),
            )

    def validate_game_data(
        self,
        game: Game,
        season_id: SeasonID,
        week: int,
        date: datetime.date,
        season_section: SeasonSection,
        home_team_id: TeamID,
        away_team_id: TeamID,
        home_team_score: Optional[int],
        away_team_score: Optional[int],
        status: GameStatus,
        notes: str,
    ) -> None:
        if game.season_id != season_id:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    f"Game.season_id does not match season_id: {game.season_id} vs."
                    f" {season_id}",
                    str(game.id_),
                    "season_id",
                    str(game.season_id),
                    str(season_id),
                ),
            )
        if game.week != week:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    f"Game.week does not match week: {game.week} vs. {week}",
                    str(game.id_),
                    "week",
                    game.week,
                    week,
                ),
            )
        if game.date != date:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    f"Game.date does not match date: {game.date} vs. {date}",
                    str(game.id_),
                    "date",
                    game.date,
                    date,
                ),
            )
        if game.season_section != season_section:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    "Game.season_section does not match season_section:"
                    f" {game.season_section} vs. {season_section}",
                    str(game.id_),
                    "season_section",
                    game.season_section.name,
                    season_section.name,
                ),
            )
        if game.home_team_id != home_team_id:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    "Game.home_team_id does not match home_team_id:"
                    f" {game.home_team_id} vs. {home_team_id}",
                    str(game.id_),
                    "home_team_id",
                    str(game.home_team_id),
                    str(home_team_id),
                ),
            )
        if game.away_team_id != away_team_id:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    "Game.away_team_id does not match away_team_id:"
                    f" {game.away_team_id} vs. {away_team_id}",
                    str(game.id_),
                    "away_team_id",
                    str(game.away_team_id),
                    str(away_team_id),
                ),
            )
        if game.home_team_score != home_team_score:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    "Game.home_team_score does not match home_team_score:"
                    f" {game.home_team_score} vs. {home_team_score}",
                    str(game.id_),
                    "home_team_score",
                    game.home_team_score,
                    home_team_score,
                ),
            )
        if game.away_team_score != away_team_score:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    "Game.away_team_score does not match away_team_score:"
                    f" {game.away_team_score} vs. {away_team_score}",
                    str(game.id_),
                    "away_team_score",
                    game.away_team_score,
                    away_team_score,
                ),
            )

        winning_team_id: Optional[TeamID]
        losing_team_id: Optional[TeamID]
        winning_team_score: Optional[int]
        losing_team_score: Optional[int]
        if home_team_score is not None and away_team_score is not None:
            if home_team_score > away_team_score:
                winning_team_id = home_team_id
                losing_team_id = away_team_id
                winning_team_score = home_team_score
                losing_team_score = away_team_score
            else:
                winning_team_id = away_team_id
                losing_team_id = home_team_id
                winning_team_score = away_team_score
                losing_team_score = home_team_score
        else:
            winning_team_id = None
            losing_team_id = None
            winning_team_score = None
            losing_team_score = None

        if game.winning_team_id != winning_team_id:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    "Game.winning_team_id does not match winning_team_id:"
                    f" {game.winning_team_id} vs. {winning_team_id}",
                    str(game.id_),
                    "winning_team_id",
                    str(game.winning_team_id),
                    str(winning_team_id),
                ),
            )
        if game.losing_team_id != losing_team_id:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    "Game.losing_team_id does not match losing_team_id:"
                    f" {game.losing_team_id} vs. {losing_team_id}",
                    str(game.id_),
                    "losing_team_id",
                    str(game.losing_team_id),
                    str(losing_team_id),
                ),
            )
        if game.winning_team_score != winning_team_score:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    "Game.winning_team_score does not match winning_team_score:"
                    f" {game.winning_team_score} vs. {winning_team_score}",
                    str(game.id_),
                    "winning_team_score",
                    game.winning_team_score,
                    winning_team_score,
                ),
            )
        if game.losing_team_score != losing_team_score:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    "Game.losing_team_score does not match losing_team_score:"
                    f" {game.losing_team_score} vs. {losing_team_score}",
                    str(game.id_),
                    "losing_team_score",
                    game.losing_team_score,
                    losing_team_score,
                ),
            )
        if game.status != status:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    f"Game.status does not match status: {game.status} vs. {status}",
                    str(game.id_),
                    "status",
                    game.status.name,
                    status.name,
                ),
            )
        if game.notes != notes:
            self._event_bus.publish(
                GameDataValidationError(
                    str(uuid4()),
                    f"Game.notes does not match notes: {game.notes} vs. {notes}",
                    str(game.id_),
                    "notes",
                    game.notes,
                    notes,
                ),
            )

    def validate_season_games(
        self,
        season_id: SeasonID,
        affiliations: Iterable[Affiliation],
        games: Iterable[Game],
    ) -> None:
        fbs_game_counts = {}
        fcs_game_counts = {}
        for affiliation in affiliations:
            if affiliation.subdivision == Subdivision.FBS:
                fbs_game_counts[affiliation.team_id] = 0
            elif affiliation.subdivision == Subdivision.FCS:
                fcs_game_counts[affiliation.team_id] = 0
            else:
                self._event_bus.publish(
                    AffiliationDataValidationError(
                        str(uuid4()),
                        f"Unknown subdivision: {affiliation.subdivision}",
                        str(affiliation.id_),
                        "subdivision",
                        affiliation.subdivision.name,
                        None,
                    ),
                )

        regular_season_game_count = 0
        postseason_game_count = 0

        for game in games:
            if game.home_team_id in fbs_game_counts:
                fbs_game_counts[game.home_team_id] += 1
            elif game.home_team_id in fcs_game_counts:
                fcs_game_counts[game.home_team_id] += 1
            else:
                self._event_bus.publish(
                    GameDataValidationError(
                        str(uuid4()),
                        "Unknown home team",
                        str(game.id_),
                        "home_team_id",
                        str(game.home_team_id),
                        None,
                    ),
                )

            if game.away_team_id in fbs_game_counts:
                fbs_game_counts[game.away_team_id] += 1
            elif game.away_team_id in fcs_game_counts:
                fcs_game_counts[game.away_team_id] += 1
            else:
                self._event_bus.publish(
                    GameDataValidationError(
                        str(uuid4()),
                        "Unknown away team",
                        str(game.id_),
                        "away_team",
                        str(game.away_team_id),
                        None,
                    ),
                )

            if game.season_section == SeasonSection.REGULAR_SEASON:
                regular_season_game_count += 1
            elif game.season_section == SeasonSection.POSTSEASON:
                postseason_game_count += 1

        for team_id, game_count in fbs_game_counts.items():
            if game_count < 10:
                self._event_bus.publish(
                    FBSGameCountValidationError(
                        str(uuid4()),
                        "FBS team has too few games",
                        str(season_id),
                        str(team_id),
                        game_count,
                    ),
                )

        for team_id, game_count in fcs_game_counts.items():
            if game_count > 5:
                self._event_bus.publish(
                    FCSGameCountValidationError(
                        str(uuid4()),
                        "FCS team had too many games",
                        str(season_id),
                        str(team_id),
                        game_count,
                    ),
                )

        postseason_percentage = float(postseason_game_count) / regular_season_game_count
        if postseason_percentage < 0.03:
            self._event_bus.publish(
                PostseasonGameCountValidationError(
                    str(uuid4()),
                    "Too few postseason games",
                    str(season_id),
                    regular_season_game_count,
                    postseason_game_count,
                ),
            )
        elif postseason_percentage > 0.06:
            self._event_bus.publish(
                PostseasonGameCountValidationError(
                    str(uuid4()),
                    "Too many postseason games",
                    str(season_id),
                    regular_season_game_count,
                    postseason_game_count,
                ),
            )
