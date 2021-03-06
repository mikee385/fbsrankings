from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.common import EventBus
from fbsrankings.infrastructure import TransactionFactory
from fbsrankings.infrastructure import UnitOfWork
from fbsrankings.infrastructure.sportsreference import SportsReference


class ImportSeasonByYearCommandHandler:
    def __init__(
        self,
        sports_reference: SportsReference,
        data_source: TransactionFactory,
        event_bus: EventBus,
    ) -> None:
        self._sports_reference = sports_reference
        self._data_source = data_source
        self._event_bus = event_bus

    def __call__(self, command: ImportSeasonByYearCommand) -> None:
        with UnitOfWork(self._data_source, self._event_bus) as unit_of_work:
            self._sports_reference.import_season(command.year, unit_of_work)

            unit_of_work.commit()
