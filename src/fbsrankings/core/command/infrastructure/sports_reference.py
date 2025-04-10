import datetime
from collections.abc import Iterator
from html.parser import HTMLParser
from typing import Any
from typing import Optional
from urllib.request import urlopen

from fbsrankings.core.command.domain.model.affiliation import Affiliation
from fbsrankings.core.command.domain.model.game import Game
from fbsrankings.core.command.domain.model.season import Season
from fbsrankings.core.command.domain.model.team import Team
from fbsrankings.core.command.domain.service.importer import Importer
from fbsrankings.core.command.domain.service.validator import Validator
from fbsrankings.messages.enums import GameStatus
from fbsrankings.messages.enums import SeasonSection
from fbsrankings.messages.enums import Subdivision


class SportsReference:
    def __init__(
        self,
        alternate_names: dict[str, str],
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
            team_soup = team_html.read().decode("utf-8")
        team_rows = _html_iter(team_soup)

        game_url = f"https://www.sports-reference.com/cfb/years/{year}-schedule.html"
        if not game_url.lower().startswith("http"):
            raise ValueError(f"Only HTTP is allowed for games URL {game_url}")

        with urlopen(game_url) as game_html:  # nosec
            game_soup = game_html.read().decode("utf-8")
        game_rows = _html_iter(game_soup)

        season = self._importer.import_season(year)

        if self._validator is not None:
            self._validator.validate_season_data(season, year)

        _, fbs_affiliations = self._import_team_rows(season, team_rows)
        games, fcs_affiliations = self._import_game_rows(season, game_rows)

        most_recent_completed_week = 0
        for game in games:
            if (
                game.status == GameStatus.GAME_STATUS_COMPLETED
                and game.week > most_recent_completed_week
            ):
                most_recent_completed_week = game.week
        for game in games:
            if (
                game.status == GameStatus.GAME_STATUS_SCHEDULED
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
        team_rows: Iterator[list[str]],
    ) -> tuple[list[Team], list[Affiliation]]:
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

                team, affiliation = self._import_team(
                    name,
                    season,
                    Subdivision.SUBDIVISION_FBS,
                )
                teams.append(team)
                fbs_affiliations.append(affiliation)

                if self._validator is not None:
                    self._validator.validate_team_data(team, name)
                    self._validator.validate_affiliation_data(
                        affiliation,
                        season.id_,
                        team.id_,
                        Subdivision.SUBDIVISION_FBS,
                    )

        return teams, fbs_affiliations

    def _import_team(
        self,
        name: str,
        season: Season,
        subdivision: Subdivision,
    ) -> tuple[Team, Affiliation]:
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
        game_rows: Iterator[list[str]],
    ) -> tuple[list[Game], list[Affiliation]]:
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
                    Subdivision.SUBDIVISION_FCS,
                )
                if home_affiliation.subdivision == Subdivision.SUBDIVISION_FCS:
                    fcs_affiliations.append(home_affiliation)

                away_team, away_affiliation = self._import_team(
                    away_team_name,
                    season,
                    Subdivision.SUBDIVISION_FCS,
                )
                if away_affiliation.subdivision == Subdivision.SUBDIVISION_FCS:
                    fcs_affiliations.append(away_affiliation)

                notes = row[notes_index].strip()

                if (home_team_name == "Army" and away_team_name == "Navy") or (
                    away_team_name == "Army" and home_team_name == "Navy"
                ):
                    army_navy_found = True
                elif " Bowl" in notes and army_navy_found:
                    postseason = True

                if postseason:
                    season_section = SeasonSection.SEASON_SECTION_POSTSEASON
                else:
                    season_section = SeasonSection.SEASON_SECTION_REGULAR_SEASON

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


class TableRowParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_tr = False
        self.in_td_or_th = False
        self.data = ""
        self.current_row: list[str] = []
        self.rows: list[list[str]] = []

    def handle_starttag(
        self,
        tag: str,
        _: list[tuple[str, Optional[str]]],
    ) -> None:
        if tag == "tr":
            self.in_tr = True
            self.current_row = []
        elif tag in ("td", "th") and self.in_tr:
            self.in_td_or_th = True
            self.data = ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr" and self.in_tr:
            self.in_tr = False
            self.rows.append(self.current_row)
        elif tag in ("td", "th") and self.in_td_or_th:
            self.in_td_or_th = False
            self.current_row.append(self.data.strip())

    def handle_data(self, data: str) -> None:
        if self.in_td_or_th:
            self.data = data

    def error(self, message: str) -> Any:
        raise ValueError(message)


def _html_iter(html_content: str) -> Iterator[list[str]]:
    parser = TableRowParser()
    parser.feed(html_content)
    yield from parser.rows
