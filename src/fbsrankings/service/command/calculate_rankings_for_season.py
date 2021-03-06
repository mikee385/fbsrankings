from uuid import UUID

from fbsrankings.command import CalculateRankingsForSeasonCommand
from fbsrankings.common import EventBus
from fbsrankings.domain import ColleyMatrixRankingService
from fbsrankings.domain import GameStrengthRankingService
from fbsrankings.domain import SeasonData
from fbsrankings.domain import SeasonID
from fbsrankings.domain import SimultaneousWinsRankingService
from fbsrankings.domain import SRSRankingService
from fbsrankings.domain import StrengthOfScheduleRankingService
from fbsrankings.domain import TeamRecordService
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure import UnitOfWork


class CalculateRankingsForSeasonCommandHandler:
    def __init__(self, data_source: TransactionFactory, event_bus: EventBus) -> None:
        self._data_source = data_source
        self._event_bus = event_bus

    def __call__(self, command: CalculateRankingsForSeasonCommand) -> None:
        with UnitOfWork(self._data_source, self._event_bus) as unit_of_work:

            if isinstance(command.season_id_or_year, UUID):
                season = unit_of_work.season.get(SeasonID(command.season_id_or_year))
            elif isinstance(command.season_id_or_year, int):
                season = unit_of_work.season.find(command.season_id_or_year)
            else:
                raise TypeError("season_id_or_year must be of type UUID or int")

            if season is None:
                raise ValueError(f"Season not found for {command.season_id_or_year}")

            teams = unit_of_work.team.all_()
            affiliations = unit_of_work.affiliation.for_season(season.id_)
            games = unit_of_work.game.for_season(season.id_)

            season_data = SeasonData(season, teams, affiliations, games)

            TeamRecordService(unit_of_work.team_record).calculate_for_season(
                season_data,
            )

            srs_rankings = SRSRankingService(
                unit_of_work.team_ranking,
            ).calculate_for_season(season_data)
            for ranking in srs_rankings:
                StrengthOfScheduleRankingService(
                    unit_of_work.team_ranking,
                ).calculate_for_ranking(season_data, ranking)
                GameStrengthRankingService(
                    unit_of_work.game_ranking,
                ).calculate_for_ranking(season_data, ranking)

            cm_rankings = ColleyMatrixRankingService(
                unit_of_work.team_ranking,
            ).calculate_for_season(season_data)
            for ranking in cm_rankings:
                StrengthOfScheduleRankingService(
                    unit_of_work.team_ranking,
                ).calculate_for_ranking(season_data, ranking)
                GameStrengthRankingService(
                    unit_of_work.game_ranking,
                ).calculate_for_ranking(season_data, ranking)

            sw_rankings = SimultaneousWinsRankingService(
                unit_of_work.team_ranking,
            ).calculate_for_season(season_data)
            for ranking in sw_rankings:
                StrengthOfScheduleRankingService(
                    unit_of_work.team_ranking,
                ).calculate_for_ranking(season_data, ranking)
                GameStrengthRankingService(
                    unit_of_work.game_ranking,
                ).calculate_for_ranking(season_data, ranking)

            unit_of_work.commit()
