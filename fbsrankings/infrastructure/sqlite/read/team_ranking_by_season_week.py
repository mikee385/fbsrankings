import sqlite3
from uuid import UUID

from fbsrankings.infrastructure.sqlite.storage import RankingTable
from fbsrankings.infrastructure.sqlite.storage import RankingType
from fbsrankings.infrastructure.sqlite.storage import SeasonTable
from fbsrankings.infrastructure.sqlite.storage import TeamRankingValueTable
from fbsrankings.infrastructure.sqlite.storage import TeamTable
from fbsrankings.query import TeamRankingBySeasonWeekQuery
from fbsrankings.query import TeamRankingBySeasonWeekResult
from fbsrankings.query import TeamRankingValueBySeasonWeekResult


class TeamRankingBySeasonWeekQueryHandler(object):
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

        self.ranking_table = RankingTable()
        self.value_table = TeamRankingValueTable()
        self.season_table = SeasonTable()
        self.team_table = TeamTable()
        
    def __call__(self, query: TeamRankingBySeasonWeekQuery) -> TeamRankingBySeasonWeekResult:
        where = "ranking.Name=? AND ranking.Type=? AND ranking.SeasonID=?"
        params = [query.name, RankingType.TEAM.name, str(query.season_ID)]
        
        if query.week is not None:
            where += " AND Week=?"
            params.append(query.week)
        else:
            where += " AND Week is NULL"
        
        cursor = self._connection.cursor()
        cursor.execute(f"SELECT ranking.UUID, ranking.Name, ranking.SeasonID, season.Year, ranking.Week FROM {self.ranking_table.name} AS ranking INNER JOIN {self.season_table.name} AS season ON season.UUID = ranking.SeasonID WHERE {where}", params)
        row = cursor.fetchone()
        
        values = []
        if row is not None:
            cursor.execute(f"SELECT value.TeamID, team.Name, value.Ord, value.Rank, value.Value FROM {self.value_table.name} AS value INNER JOIN {self.team_table.name} AS team ON team.UUID = value.TeamID WHERE value.RankingID=?", [row[0]])
            values = [TeamRankingValueBySeasonWeekResult(UUID(value[0]), value[1], value[2], value[3], value[4]) for value in cursor.fetchall()]
        
        cursor.close()
        
        if row is not None:
            return TeamRankingBySeasonWeekResult(UUID(row[0]), row[1], UUID(row[2]), row[3], row[4], values)
        else:
            return None

