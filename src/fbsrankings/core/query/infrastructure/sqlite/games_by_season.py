import sqlite3
from datetime import datetime

from fbsrankings.messages.convert import datetime_to_timestamp
from fbsrankings.messages.query import GameBySeasonResult
from fbsrankings.messages.query import GamesBySeasonQuery
from fbsrankings.messages.query import GamesBySeasonResult
from fbsrankings.storage.sqlite import GameTable
from fbsrankings.storage.sqlite import SeasonTable
from fbsrankings.storage.sqlite import TeamTable


class GamesBySeasonQueryHandler:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self._season_table = SeasonTable().table
        self._team_table = TeamTable().table
        self._game_table = GameTable().table

    def __call__(self, query: GamesBySeasonQuery) -> GamesBySeasonResult:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT "
            f"{self._game_table}.UUID, "
            f"{self._game_table}.SeasonID, "
            f"{self._season_table}.Year, "
            f"{self._game_table}.Week, "
            f"{self._game_table}.Date, "
            f"{self._game_table}.SeasonSection, "
            f"{self._game_table}.HomeTeamID, "
            "home_team.Name, "
            f"{self._game_table}.AwayTeamID, "
            "away_team.Name, "
            f"{self._game_table}.HomeTeamScore, "
            f"{self._game_table}.AwayTeamScore, "
            f"{self._game_table}.Status, "
            f"{self._game_table}.Notes "
            f"FROM {self._game_table} "
            f"JOIN {self._season_table} "
            f"ON {self._season_table}.UUID = {self._game_table}.SeasonID "
            f"JOIN {self._team_table} home_team "
            f"ON home_team.UUID = {self._game_table}.HomeTeamID "
            f"JOIN {self._team_table} away_team "
            f"ON away_team.UUID = {self._game_table}.AwayTeamID "
            f"WHERE {self._game_table}.SeasonID = ?;",
            [query.season_id],
        )
        items = [
            GameBySeasonResult(
                game_id=row[0],
                season_id=row[1],
                year=row[2],
                week=row[3],
                date=datetime_to_timestamp(datetime.strptime(row[4], "%Y-%m-%d")),
                season_section=row[5],
                home_team_id=row[6],
                home_team_name=row[7],
                away_team_id=row[8],
                away_team_name=row[9],
                home_team_score=row[10],
                away_team_score=row[11],
                status=row[12],
                notes=row[13],
            )
            for row in cursor.fetchall()
        ]
        cursor.close()

        return GamesBySeasonResult(query_id=query.query_id, games=items)
