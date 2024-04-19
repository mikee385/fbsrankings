import datetime
from typing import Dict
from typing import Iterator
from typing import List
from typing import Tuple
from urllib.request import urlopen

from bs4 import BeautifulSoup
from bs4 import Tag

from fbsrankings.core.command.domain.model.affiliation import Affiliation
from fbsrankings.core.command.domain.model.game import Game
from fbsrankings.core.command.domain.model.season import Season
from fbsrankings.core.command.domain.model.team import Team
from fbsrankings.core.command.domain.service.importer import Importer
from fbsrankings.core.command.domain.service.validator import Validator
from fbsrankings.enums import GameStatus
from fbsrankings.enums import SeasonSection
from fbsrankings.enums import Subdivision


class SportsReference:
    def __init__(
        self,
        alternate_names: Dict[str, str],
        importer: Importer,
        validator: Validator,
    ) -> None:
        if alternate_names is not None:
            self._alternate_names = {
                key.lower(): value for key, value in alternate_names.items()
            }
        else:
            self._alternate_names = {}

        self._importer = importer
        self._validator = validator

    def import_season(self, year: int) -> None:
        team_url = f"https://www.sports-reference.com/cfb/years/{year}-standings.html"
        if not team_url.lower().startswith("http"):
            raise ValueError(f"Only HTTP is allowed for teams URL {team_url}")

        with urlopen(team_url) as team_html:  # nosec
            team_soup = BeautifulSoup(team_html, "html5lib")
        team_rows = _html_iter(team_soup)

        game_url = f"https://www.sports-reference.com/cfb/years/{year}-schedule.html"
        if not game_url.lower().startswith("http"):
            raise ValueError(f"Only HTTP is allowed for games URL {game_url}")

        with urlopen(game_url) as game_html:  # nosec
            game_soup = BeautifulSoup(game_html, "html5lib")
        game_rows = _html_iter(game_soup)

        season = self._importer.import_season(year)

        if self._validator is not None:
            self._validator.validate_season_data(season, year)

        _, fbs_affiliations = self._import_team_rows(season, team_rows)
        games, fcs_affiliations = self._import_game_rows(season, game_rows)

        most_recent_completed_week = 0
        for game in games:
            if (
                game.status == GameStatus.COMPLETED
                and game.week > most_recent_completed_week
            ):
                most_recent_completed_week = game.week
        for game in games:
            if (
                game.status == GameStatus.SCHEDULED
                and game.week < most_recent_completed_week
            ):
                game.cancel()

        if self._validator is not None:
            self._validator.validate_season_games(
                season.id_,
                fbs_affiliations + fcs_affiliations,
                games,
            )

    def _import_team_rows(
        self,
        season: Season,
        team_rows: Iterator[List[str]],
    ) -> Tuple[List[Team], List[Affiliation]]:
        header_row = next(team_rows)
        if header_row[0] == "":
            header_row = next(team_rows)

        rank_index = header_row.index("Rk")
        name_index = header_row.index("School")

        teams = []
        fbs_affiliations = []
        for row in team_rows:
            if row[rank_index].isdigit():
                name = row[name_index].strip()

                alternate_name = self._alternate_names.get(name.lower())
                if alternate_name:
                    name = alternate_name

                team, affiliation = self._import_team(name, season, Subdivision.FBS)
                teams.append(team)
                fbs_affiliations.append(affiliation)

                if self._validator is not None:
                    self._validator.validate_team_data(team, name)
                    self._validator.validate_affiliation_data(
                        affiliation,
                        season.id_,
                        team.id_,
                        Subdivision.FBS,
                    )

        return teams, fbs_affiliations

    def _import_team(
        self,
        name: str,
        season: Season,
        subdivision: Subdivision,
    ) -> Tuple[Team, Affiliation]:
        team = self._importer.import_team(name)

        if self._validator is not None:
            self._validator.validate_team_data(
                team,
                name,
            )

        affiliation = self._importer.import_affiliation(
            season.id_,
            team.id_,
            subdivision,
        )

        if self._validator is not None:
            self._validator.validate_affiliation_data(
                affiliation,
                season.id_,
                team.id_,
                affiliation.subdivision,
            )

        return team, affiliation

    def _import_game_rows(
        self,
        season: Season,
        game_rows: Iterator[List[str]],
    ) -> Tuple[List[Game], List[Affiliation]]:
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

        army_navy_found = False
        postseason = False

        games = []
        fcs_affiliations = []
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

                alternate_name = self._alternate_names.get(first_team_name.lower())
                if alternate_name:
                    first_team_name = alternate_name

                if first_score_string == "":
                    first_score = None
                else:
                    first_score = int(first_score_string)

                if second_team_name.startswith("("):
                    start = second_team_name.find(")")
                    second_team_name = second_team_name[start + 2 :].strip()

                alternate_name = self._alternate_names.get(second_team_name.lower())
                if alternate_name:
                    second_team_name = alternate_name

                if second_score_string == "":
                    second_score = None
                else:
                    second_score = int(second_score_string)

                if home_away_symbol in ("", "N"):
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

                home_team, home_affiliation = self._import_team(
                    home_team_name,
                    season,
                    Subdivision.FCS,
                )
                if home_affiliation.subdivision == Subdivision.FCS:
                    fcs_affiliations.append(home_affiliation)

                away_team, away_affiliation = self._import_team(
                    away_team_name,
                    season,
                    Subdivision.FCS,
                )
                if away_affiliation.subdivision == Subdivision.FCS:
                    fcs_affiliations.append(away_affiliation)

                notes = row[notes_index].strip()

                if (home_team_name == "Army" and away_team_name == "Navy") or (
                    away_team_name == "Army" and home_team_name == "Navy"
                ):
                    army_navy_found = True
                elif " Bowl" in notes and army_navy_found:
                    postseason = True

                if postseason:
                    season_section = SeasonSection.POSTSEASON
                else:
                    season_section = SeasonSection.REGULAR_SEASON

                game = self._importer.import_game(
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
                games.append(game)

                if self._validator is not None:
                    self._validator.validate_game_data(
                        game,
                        season.id_,
                        week,
                        date,
                        season_section,
                        home_team.id_,
                        away_team.id_,
                        home_team_score,
                        away_team_score,
                        game.status,
                        notes,
                    )

        return games, fcs_affiliations


def _html_iter(soup: BeautifulSoup) -> Iterator[List[str]]:
    row_iter = iter(soup.find_all("tr"))
    for row in row_iter:
        yield [
            child.getText()
            for child in filter(lambda c: isinstance(c, Tag), row.children)
        ]
