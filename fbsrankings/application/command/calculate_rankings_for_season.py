from uuid import UUID

from fbsrankings.command import CalculateRankingsForSeasonCommand
from fbsrankings.common import EventBus
from fbsrankings.domain import ColleyMatrixRankingService
from fbsrankings.domain import SeasonData
from fbsrankings.domain import SeasonID
from fbsrankings.domain import SimultaneousWinsRankingService
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure import UnitOfWork


class CalculateRankingsForSeasonCommandHandler(object):
    def __init__(self, data_source: TransactionFactory, event_bus: EventBus) -> None:
        self._data_source = data_source
        self._event_bus = event_bus

    def __call__(self, command: CalculateRankingsForSeasonCommand) -> None:
        with UnitOfWork(self._data_source, self._event_bus) as unit_of_work:

            if isinstance(command.season_ID_or_year, UUID):
                season = unit_of_work.season.get(SeasonID(command.season_ID_or_year))
            elif isinstance(command.season_ID_or_year, int):
                season = unit_of_work.season.find(command.season_ID_or_year)
            else:
                raise TypeError("season_ID_or_year must be of type UUID or int")

            if season is None:
                raise ValueError(f"Season not found for {command.season_ID_or_year}")

            teams = unit_of_work.team.all()
            affiliations = unit_of_work.affiliation.for_season(season.ID)
            games = unit_of_work.game.for_season(season.ID)

            season_data = SeasonData(season, teams, affiliations, games)
            ColleyMatrixRankingService(unit_of_work.ranking).calculate_for_season(
                season.ID, season_data
            )
            SimultaneousWinsRankingService(unit_of_work.ranking).calculate_for_season(
                season.ID, season_data
            )

            unit_of_work.commit()
