from fbsrankings.domain import GameStatus


class CancelService (object):
    def cancel_past_games(self, games):
        most_recent_completed_week_by_season = {}
        for game in games:
            if game.status == GameStatus.COMPLETED:
                most_recent_completed_week = most_recent_completed_week_by_season.get(game.season_ID)
                if most_recent_completed_week is not None:
                    if game.week > most_recent_completed_week:
                        most_recent_completed_week_by_season[game.season_ID] = game.week
                else:
                    most_recent_completed_week_by_season[game.season_ID] = game.week
                    
        for game in games:
            if game.status == GameStatus.SCHEDULED:
                most_recent_completed_week = most_recent_completed_week_by_season.get(game.season_ID)
                if most_recent_completed_week is not None and game.week < most_recent_completed_week:
                    game.cancel()
