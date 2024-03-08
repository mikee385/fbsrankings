from fbsrankings.infrastructure.memory.storage import Storage
from fbsrankings.query import AffiliationBySeasonResult
from fbsrankings.query import AffiliationsBySeasonQuery
from fbsrankings.query import AffiliationsBySeasonResult


class AffiliationsBySeasonQueryHandler:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def __call__(self, query: AffiliationsBySeasonQuery) -> AffiliationsBySeasonResult:
        season = self._storage.season.get(query.season_id)
        teams = {team.id_: team for team in self._storage.team.all_()}
        affiliations = self._storage.affiliation.for_season(query.season_id)

        items = []
        for affiliation in affiliations:
            team = teams.get(affiliation.team_id)

            if season is not None and team is not None:
                items.append(
                    AffiliationBySeasonResult(
                        affiliation.id_,
                        affiliation.season_id,
                        season.year,
                        affiliation.team_id,
                        team.name,
                        affiliation.subdivision,
                    ),
                )

        return AffiliationsBySeasonResult(items)
