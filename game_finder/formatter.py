import blaseball_core_game_data as gd
from .util import sanitize_dale
import os
import time
import json

class NoGamesException(Exception):
    pass

class BaseFormatter(object):
    def __init__(self, options):
        """Load the data set"""
        self.data = json.loads(gd.get_games_data())
        self.options = options

        # user provides one-indexed days and seasons
        # data has zero-indexed days and seasons
        if 'all' not in options.season:
            self.seasons = [str(int(j)-1) for j in options.season]

        if options.day:
            self.days = [str(int(j)-1) for j in options.day]
        else:
            self.days = None

        self.our_team = [sanitize_dale(j) for j in options.team]
        self.their_team = [sanitize_dale(j) for j in options.versus_team]

        # data is a list of dictionaries
        # keys:
        # - awayOdds
        # - awayPitcherName
        # - awayScore
        # - awayTeamEmoji
        # - awayTeamName
        # - awayTeamNickname
        # - day
        # - homeOdds
        # - homePitcherName
        # - homeScore
        # - homeTeamEmoji
        # - homeTeamName
        # - homeTeamNickname
        # - id
        # - isPostseason
        # - losingOdds
        # - losingPitcherName
        # - losingScore
        # - losingTeamEmoji
        # - losingTeamName
        # - losingTeamNickname
        # - runDiff
        # - season
        # - shame
        # - whoWon
        # - winningOdds
        # - winningPitcherName
        # - winningScore
        # - winningTeamEmoji
        # - winningTeamName
        # - winningTeamNickname

        # use list comprehensions to do fast filtering
        # but first, write the loops explicitly

        # UUUURRRRRGGGGGGGGGGGG for some reason all the Dale 
        # are getting switched from unicode format (when we import)
        # to plain string format (below). BUT HOW???

        # Seasons filter
        if 'all' not in options.season:
            new_data = []
            for game in self.data:
                if str(game['season']) in self.seasons:
                    new_data.append(game)
            self.data = new_data

        # Days filter
        if self.days is not None:
            new_data = []
            for game in self.data:
                if str(game['day']) in self.days:
                    new_data.append(game)
            self.data = new_data

        # Teams filter
        new_data = []
        for game in self.data:
            b1 = lambda g: g['awayTeamNickname'] in self.our_team and g['homeTeamNickname'] in self.their_team
            b2 = lambda g: g['homeTeamNickname'] in self.our_team and g['awayTeamNickname'] in self.their_team 
            if b1(game) or b2(game):
                new_data.append(game)
        self.data = new_data

        # Postseason filter
        if options.postseason:
            new_data = []
            for game in self.data:
                if game['isPostseason']:
                    new_data.append(game)
            self.data = new_data


class JsonFormatter(BaseFormatter):
    def output(self):
        data_short = []
        for game in self.data:
            game_short = {}
            short_keys = ['awayOdds','awayScore','awayTeamNickname','day','homeOdds','homeScore','homeTeamNickname','id','isPostseason','whoWon','shame','season','runDiff']
            for k in short_keys:
                game_short[k] = game[k]
            data_short.append(game_short)
        print(json.dumps(data_short, indent=4))

class TextFormatter(BaseFormatter):
    def output(self):
        for game in self.data:
            print(game['id'])
