from fbsrankings.messages.query import AffiliationBySeasonResult
from fbsrankings.messages.query import AffiliationsBySeasonQuery
from fbsrankings.messages.query import AffiliationsBySeasonResult
from fbsrankings.storage.memory import Storage


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
                        str(affiliation.id_),
                        str(affiliation.season_id),
                        season.year,
                        str(affiliation.team_id),
                        team.name,
                        affiliation.subdivision,
                    ),
                )

        return AffiliationsBySeasonResult(items)
