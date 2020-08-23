import datetime
from abc import ABCMeta
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from urllib.request import urlopen

from bs4 import BeautifulSoup
from bs4 import Tag
from dataclasses import dataclass  # pylint: disable=wrong-import-order
from typing_extensions import Protocol

from fbsrankings.domain import Affiliation
from fbsrankings.domain import AffiliationRepository
from fbsrankings.domain import Game
from fbsrankings.domain import GameRepository
from fbsrankings.domain import GameStatus
from fbsrankings.domain import Season
from fbsrankings.domain import SeasonID
from fbsrankings.domain import SeasonRepository
from fbsrankings.domain import SeasonSection
from fbsrankings.domain import Subdivision
from fbsrankings.domain import Team
from fbsrankings.domain import TeamID
from fbsrankings.domain import TeamRepository
from fbsrankings.domain import ValidationService


class RepositoryManager(Protocol, metaclass=ABCMeta):
    @property
    def season(self) -> SeasonRepository:
        raise NotImplementedError

    @property
    def team(self) -> TeamRepository:
        raise NotImplementedError

    @property
    def affiliation(self) -> AffiliationRepository:
        raise NotImplementedError

    @property
    def game(self) -> GameRepository:
        raise NotImplementedError


@dataclass(frozen=True)
class _SeasonSource:
    year: int
    postseason_start_week: int
    source_type: str
    team_source: str
    game_source: str


_TeamCache = Dict[str, Team]
_AffiliationCache = Dict[Tuple[SeasonID, TeamID], Affiliation]
_GameCache = Dict[Tuple[SeasonID, int, TeamID, TeamID], Game]


class _Cache:
    def __init__(self) -> None:
        self.team: _TeamCache = {}
        self.affiliation: _AffiliationCache = {}
        self.game: _GameCache = {}


class SportsReference:
    def __init__(
        self, alternate_names: Dict[str, str], validation_service: ValidationService,
    ) -> None:
        self._sources: Dict[int, _SeasonSource] = {}

        if alternate_names is not None:
            self._alternate_names = {key.lower(): value for key, value in alternate_names.items()}
        else:
            self._alternate_names = {}

        self._validation_service = validation_service

    def add_source(
        self,
        year: int,
        postseason_start_week: int,
        source_type: str,
        team_source: str,
        game_source: str,
    ) -> None:
        if self._sources.get(year) is not None:
            raise ValueError(f"Source already exists for year {year}")

        self._sources[year] = _SeasonSource(
            year, postseason_start_week, source_type, team_source, game_source,
        )

    def import_season(self, year: int, repository: RepositoryManager) -> None:
        source = self._sources.get(year)
        if source is None:
            raise ValueError(f"Source has not been added for year {year}")

        if not source.team_source.lower().startswith("http"):
            raise ValueError(f"Only HTTP is allowed for teams URL {source.team_source}")

        team_html = urlopen(source.team_source)  # nosec
        team_soup = BeautifulSoup(team_html, "html5lib")
        team_rows = _html_iter(team_soup)

        if not source.game_source.lower().startswith("http"):
            raise ValueError(f"Only HTTP is allowed for games URL {source.game_source}")

        game_html = urlopen(source.game_source)  # nosec
        game_soup = BeautifulSoup(game_html, "html5lib")
        game_rows = _html_iter(game_soup)

        season = self._import_season(repository.season, source.year)

        cache = _Cache()
        self._import_team_rows(team_rows, season, repository, cache)
        self._import_game_rows(
            game_rows, season, source.postseason_start_week, repository, cache,
        )

        most_recent_completed_week = 0
        for game in cache.game.values():
            if game.status == GameStatus.COMPLETED:
                if game.week > most_recent_completed_week:
                    most_recent_completed_week = game.week
        for game in cache.game.values():
            if game.status == GameStatus.SCHEDULED:
                if game.week < most_recent_completed_week:
                    game.cancel()

        if self._validation_service is not None:
            self._validation_service.validate_season_games(
                season.id_, cache.affiliation.values(), cache.game.values(),
            )

    def _import_team_rows(
        self,
        team_rows: Iterator[List[str]],
        season: Season,
        repository: RepositoryManager,
        cache: _Cache,
    ) -> None:
        header_row = next(team_rows)
        if header_row[0] == "":
            header_row = next(team_rows)

        rank_index = header_row.index("Rk")
        name_index = header_row.index("School")

        for row in team_rows:
            if row[rank_index].isdigit():
                name = row[name_index].strip()
                if name.lower() in self._alternate_names:
                    name = self._alternate_names[name.lower()]
                team = self._import_team(repository.team, cache.team, name)
                self._import_affiliation(
                    repository.affiliation,
                    cache.affiliation,
                    season.id_,
                    team.id_,
                    Subdivision.FBS,
                )

    def _import_game_rows(
        self,
        game_rows: Iterator[List[str]],
        season: Season,
        postseason_start_week: int,
        repository: RepositoryManager,
        cache: _Cache,
    ) -> None:
        header_row = next(game_rows)
        if header_row[0] == "":
            header_row = next(game_rows)

        rank_index = header_row.index("Rk")
        week_index = header_row.index("Wk")
        date_index = header_row.index("Date")
        notes_index = header_row.index("Notes")

        first_team_index = [
            index
            for index, column in enumerate(header_row)
            if column.startswith("Winner")
        ][0]

        first_score_index = first_team_index + 1

        second_team_index = [
            index
            for index, column in enumerate(header_row)
            if column.startswith("Loser")
        ][0]

        second_score_index = second_team_index + 1

        home_away_index = first_score_index + 1

        for counter, row in enumerate(game_rows):
            if row[rank_index].isdigit():
                week_string = row[week_index].strip()
                date_string = row[date_index].strip()
                first_team_name = row[first_team_index].strip()
                first_score_string = row[first_score_index].strip()
                home_away_symbol = row[home_away_index].strip()
                second_team_name = row[second_team_index].strip()
                second_score_string = row[second_score_index].strip()

                week = int(week_string)

                try:
                    date = datetime.datetime.strptime(date_string, "%b %d %Y").date()
                except ValueError:
                    date = datetime.datetime.strptime(date_string, "%b %d, %Y").date()

                if first_team_name.startswith("("):
                    start = first_team_name.find(")")
                    first_team_name = first_team_name[start + 2 :].strip()

                if first_team_name.lower() in self._alternate_names:
                    first_team_name = self._alternate_names[first_team_name.lower()]

                if first_score_string == "":
                    first_score = None
                else:
                    first_score = int(first_score_string)

                if second_team_name.startswith("("):
                    start = second_team_name.find(")")
                    second_team_name = second_team_name[start + 2 :].strip()

                if second_team_name.lower() in self._alternate_names:
                    second_team_name = self._alternate_names[second_team_name.lower()]

                if second_score_string == "":
                    second_score = None
                else:
                    second_score = int(second_score_string)

                if home_away_symbol == "":
                    home_team_name = first_team_name
                    home_team_score = first_score
                    away_team_name = second_team_name
                    away_team_score = second_score
                elif home_away_symbol == "@":
                    away_team_name = first_team_name
                    away_team_score = first_score
                    home_team_name = second_team_name
                    home_team_score = second_score
                else:
                    raise ValueError(
                        f'Unable to convert symbol "{home_away_symbol}" to an "@" on'
                        f" line {counter}",
                    )

                home_team = self._import_team(
                    repository.team, cache.team, home_team_name,
                )
                self._import_affiliation(
                    repository.affiliation,
                    cache.affiliation,
                    season.id_,
                    home_team.id_,
                    Subdivision.FCS,
                )

                away_team = self._import_team(
                    repository.team, cache.team, away_team_name,
                )
                self._import_affiliation(
                    repository.affiliation,
                    cache.affiliation,
                    season.id_,
                    away_team.id_,
                    Subdivision.FCS,
                )

                notes = row[notes_index].strip()

                if week >= postseason_start_week:
                    season_section = SeasonSection.POSTSEASON
                else:
                    season_section = SeasonSection.REGULAR_SEASON

                self._import_game(
                    repository.game,
                    cache.game,
                    season.id_,
                    week,
                    date,
                    season_section,
                    home_team.id_,
                    away_team.id_,
                    home_team_score,
                    away_team_score,
                    notes,
                )

    def _import_season(self, repository: SeasonRepository, year: int) -> Season:
        season = repository.find(year)
        if season is None:
            season = repository.create(year)

        if self._validation_service is not None:
            self._validation_service.validate_season_data(season, year)

        return season

    def _import_team(
        self, repository: TeamRepository, cache: _TeamCache, name: str,
    ) -> Team:
        key = name

        team = cache.get(key)
        if team is None:
            team = repository.find(name)
            if team is None:
                team = repository.create(name)
            cache[key] = team

        if self._validation_service is not None:
            self._validation_service.validate_team_data(team, name)

        return team

    def _import_affiliation(
        self,
        repository: AffiliationRepository,
        cache: _AffiliationCache,
        season_id: SeasonID,
        team_id: TeamID,
        subdivision: Subdivision,
    ) -> Affiliation:
        key = (season_id, team_id)

        affiliation = cache.get(key)
        if affiliation is None:
            affiliation = repository.find(season_id, team_id)
            if affiliation is None:
                affiliation = repository.create(season_id, team_id, subdivision)
            cache[key] = affiliation

        if self._validation_service is not None:
            self._validation_service.validate_affiliation_data(
                affiliation, season_id, team_id, affiliation.subdivision,
            )

        return affiliation

    def _import_game(
        self,
        repository: GameRepository,
        cache: _GameCache,
        season_id: SeasonID,
        week: int,
        date: datetime.date,
        season_section: SeasonSection,
        home_team_id: TeamID,
        away_team_id: TeamID,
        home_team_score: Optional[int],
        away_team_score: Optional[int],
        notes: str,
    ) -> Game:
        if home_team_id < away_team_id:
            key = (season_id, week, home_team_id, away_team_id)
        else:
            key = (season_id, week, away_team_id, home_team_id)

        game = cache.get(key)
        if game is None:
            game = repository.find(season_id, week, home_team_id, away_team_id)
            if game is None:
                game = repository.create(
                    season_id,
                    week,
                    date,
                    season_section,
                    home_team_id,
                    away_team_id,
                    notes,
                )
            cache[key] = game

        if date != game.date:
            game.reschedule(week, date)

        if (
            home_team_score is not None
            and away_team_score is not None
            and game.status != GameStatus.COMPLETED
        ):
            game.complete(home_team_score, away_team_score)

        if notes != game.notes:
            game.update_notes(notes)

        if self._validation_service is not None:
            self._validation_service.validate_game_data(
                game,
                season_id,
                week,
                date,
                season_section,
                home_team_id,
                away_team_id,
                home_team_score,
                away_team_score,
                game.status,
                notes,
            )

        return game


def _html_iter(soup: BeautifulSoup) -> Iterator[List[str]]:
    row_iter = iter(soup.find_all("tr"))
    for row in row_iter:
        yield [
            child.getText()
            for child in filter(lambda c: isinstance(c, Tag), row.children)
        ]
