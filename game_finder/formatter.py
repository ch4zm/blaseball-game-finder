import os
import time
import json
from .util import sanitize_dale, desanitize_dale
from .finderdata import RawDayData, NoMatchingGames


class BaseFormatter(object):
    def __init__(self, options):
        """Extract options"""
        self.options = options
        self.teams = options.team
        self.versus_teams = options.versus_team
        self.seasons = options.season
        if options.day:
            self.days = options.day
        else:
            self.days = range(1,99+1)
        self.playoffs = options.playoffs
        if self.playoffs:
            # Presumably, the max day we can reach in blaseball
            # is 15 (5 games per series times 3 rounds)
            # Add 3 just to be sure
            MAXDAYS = 115
            self.days = range(100,MAXDAYS+1+3)

    def extract(self):
        games = []
        for season in self.seasons:
            for day in self.days:
                if self.playoffs:
                    try:
                        raw_data = RawDayData(season, day)
                    except NoMatchingGames:
                        continue
                else:
                    raw_data = RawDayData(season, day)
                team_data = raw_data.get_games_by_team(self.teams, self.versus_teams)
                games += team_data
        return games

class JsonFormatter(BaseFormatter):
    def output(self):
        games_list = []
        team_data = self.extract()
        for game in self.extract().next():
            games_list.append(game)
        print(json.dumps(games_list, indent=4))

class TextFormatter(BaseFormatter):
    def output(self):
        for game in self.extract():
            print(game['id'])

# Formatter creates one RawDayData object per day
# Use the filters and figure out what days need to be included.

