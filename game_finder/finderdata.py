import requests
import json
from functools import lru_cache


class ApiError(Exception):
    pass


class NoMatchingGames(Exception):
    pass


class RawDayData(object):
    """
    This class uses the /games api endpoint and passes
    a season and a day, which returns a list of json objects,
    one per game (10 total in regular season).

    This object strips out the necessary information,
    making it available to the formatter object.
    """
    ENDPOINT = "https://blaseball.com/database/games?day={day}&season={season}"

    def __init__(self, season, day):
        url = self.ENDPOINT.format(season=season, day=day)
        resp = requests.get(url)
        if resp.status_code != 200:
            raise ApiError()
        try:
            self.games_data = resp.json()
        except JSONDecodeError:
            raise NoMatchingGames()
        if len(self.games_data)==0:
            raise NoMatchingGames()

    def get_games_by_team(self, teams, versus_teams):
        team_data = []
        for game in self.games_data:
            b1 = (game['homeTeamNickname'] in teams) and (game['awayTeamNickname'] in versus_teams)
            b2 = (game['awayTeamNickname'] in teams) and (game['homeTeamNickname'] in versus_teams)
            if b1 or b2:
                team_data.append(game)
        return team_data



