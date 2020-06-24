import json

from fbsrankings.application import Application
from fbsrankings.command import ImportSeasonByYearCommand
from fbsrankings.common import EventBus, EventCounter
from fbsrankings.domain import (
    FBSGameCountValidationError,
    FCSGameCountValidationError,
    GameDataValidationError,
)
from fbsrankings.query import (
    AffiliationCountBySeasonQuery,
    CanceledGamesQuery,
    GameByIDQuery,
    GameCountBySeasonQuery,
    SeasonByIDQuery,
    SeasonsQuery,
    TeamByIDQuery,
    TeamCountBySeasonQuery,
)

with open("config.json") as config_file:
    config = json.load(config_file)

event_bus = EventCounter(EventBus())

with Application(config, event_bus) as application:
    for year in application.seasons:
        print(f"{year}: Importing Data")
        application.send(ImportSeasonByYearCommand(year))

    print()

    seasons = application.query(SeasonsQuery()).seasons
    print(f"Total Seasons: {len(seasons)}")
    for season in seasons:
        print()
        print(f"{season.year} Season:")

        team_count = application.query(TeamCountBySeasonQuery(season.ID))
        print(f"Total Teams: {team_count.count}")

        affiliation_count = application.query(AffiliationCountBySeasonQuery(season.ID))
        print(f"FBS Teams: {affiliation_count.fbs_count}")
        print(f"FCS Teams: {affiliation_count.fcs_count}")

        game_count = application.query(GameCountBySeasonQuery(season.ID))
        print(f"Total Games: {game_count.count}")

    canceled_games = application.query(CanceledGamesQuery()).games
    if canceled_games:
        print()
        print("Canceled Games:")
        for canceled_game in canceled_games:
            print()
            print(f"Year {canceled_game.year}, Week {canceled_game.week}")
            print(canceled_game.date)
            print(canceled_game.season_section)
            print(f"{canceled_game.home_team_name} vs. {canceled_game.away_team_name}")
            print(canceled_game.notes)

    fbs_team_errors = []
    fcs_team_errors = []
    game_errors = []
    other_errors = []
    for error in application.errors:
        if isinstance(error, FBSGameCountValidationError):
            fbs_team_errors.append(error)
        elif isinstance(error, FCSGameCountValidationError):
            fcs_team_errors.append(error)
        elif isinstance(error, GameDataValidationError):
            game_errors.append(error)
        else:
            other_errors.append(error)

    if fbs_team_errors:
        print()
        print("FBS teams with too few games:")
        print()
        for error in fbs_team_errors:
            error_season = application.query(SeasonByIDQuery(error.season_ID))
            error_team = application.query(TeamByIDQuery(error.team_ID))
            if error_season is not None and error_team is not None:
                print(f"{error_season.year} {error_team.name}: {error.game_count}")

    if fcs_team_errors:
        print()
        print("FCS teams with too many games:")
        print()
        for error in fcs_team_errors:
            error_season = application.query(SeasonByIDQuery(error.season_ID))
            error_team = application.query(TeamByIDQuery(error.team_ID))
            if error_season is not None and error_team is not None:
                print(f"{error_season.year} {error_team.name}: {error.game_count}")

    if game_errors:
        print()
        print("Game Errors:")
        for error in game_errors:
            error_game = application.query(GameByIDQuery(error.game_ID))
            if error_game is not None:
                print()
                print(f"Year {error_game.year}, Week {error_game.week}")
                print(error_game.date)
                print(error_game.season_section)
                print(f"{error_game.home_team_name} vs. {error_game.away_team_name}")
                if (
                    error_game.home_team_score is not None
                    and error_game.away_team_score is not None
                ):
                    print(
                        f"{error_game.status}, {error_game.home_team_score} to {error_game.away_team_score}"
                    )
                else:
                    print(error_game.status)
                print(error_game.notes)
                print(
                    f"For {error.attribute_name}, expected: {error.expected_value}, found: {error.attribute_value}"
                )

    if other_errors:
        print()
        print("Other Errors:")
        print()
        for error in other_errors:
            print(error)

    print()
    print("Events:")
    print()
    if event_bus.counts:
        for event, count in event_bus.counts.items():
            print(f"{event.__name__}: {count}")
    else:
        print("None")

    print()
