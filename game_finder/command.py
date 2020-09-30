import sys
import os
import json
import configargparse
from io import StringIO
from .formatter import TextFormatter, JsonFormatter
from .util import (
    desanitize_dale,
    get_league_division_team_data,
    league_to_teams,
    division_to_teams,
    CaptureStdout
)


def main(sysargs = sys.argv[1:]):

    p = configargparse.ArgParser()

    # These are safe for command line usage (no accent in Dale)
    LEAGUES, DIVISIONS, ALLTEAMS = get_league_division_team_data()

    p.add('-v',
          '--version',
          required=False,
          default=False,
          action='store_true',
          help='Print program name and version number and exit')

    p.add('-c',
          '--config',
          required=False,
          is_config_file=True,
          help='config file path')

    # Pick our team
    h = p.add_mutually_exclusive_group()
    h.add('--team',
          choices=ALLTEAMS,
          action='append',
          help='Specify our team (use flag multiple times for multiple teams)')
    h.add('--division',
          choices=DIVISIONS,
          action='append',
          help='Specify our division (use flag multiple times for multiple divisions)')
    h.add('--league',
          choices=LEAGUES,
          action='append',
          help='Specify our league')

    # Pick versus team
    k = p.add_mutually_exclusive_group()
    k.add('--versus-team',
          choices=ALLTEAMS,
          action='append',
          help='Specify versus team (use flag multiple times for multiple teams)')
    k.add('--versus-division',
          choices=DIVISIONS,
          action='append',
          help='Specify versus division (use flag multiple times for multiple divisions)')
    k.add('--versus-league',
          choices=LEAGUES,
          action='append',
          help='Specify versus league')

    # Specify what season data to view
    p.add('--season',
          required=False,
          action='append',
          help='Specify season (use flag multiple times for multiple seasons, no --seasons flag means all data)')
    p.add('--day',
          required=False,
          action='append',
          help='Specify day (use flag multiple times for multiple days, no --days flag means all days)')

    # Restrict to postseason data only
    p.add('--postseason',
          action='store_true',
          default=False,
          help='Restrict game IDs to postseason games only')

    # format
    p.add('--text',
          action='store_true',
          default=False,
          help='Print game IDs in plain text format, one ID per line')
    p.add('--json',
          action='store_true',
          default=False,
          help='Print game IDs in JSON format, with additional data about the game')

    # -----

    # Print help, if no arguments provided
    if len(sysargs)==0:
        p.print_help()
        exit(0)
    elif '-v' in sysargs or '--version' in sysargs:
        # If the user asked for the version,
        # print the version number and exit.
        # (Note: this is done separate from
        # argparse, because otherwise the user
        # has to ALSO provide a game ID to get
        # the --version flag to work. ugh.)
        from . import _program, __version__
        print(_program, __version__)
        sys.exit(0)

    # Parse arguments
    options = p.parse_args(sysargs)

    # If the user specified a division or a league,
    # turn that into a list of teams for them
    if options.division:
        divteams = []
        for div in options.division:
            divteams += division_to_teams(div)
        options.team = divteams
        options.division = None
    if options.league:
        leateams = []
        for lea in options.league:
            leateams += league_to_teams(lea)
        options.team = leateams
        options.league = None
    # Same for versus
    if options.versus_division:
        vdivteams = []
        for div in options.versus_division:
            vdivteams += division_to_teams(div)
        options.versus_team = vdivteams
        options.versus_division = None
    if options.versus_league:
        vleateams = []
        for lea in options.versus_league:
            vleateams += league_to_teams(lea)
        options.versus_team = vleateams
        options.versus_league = None

    # If nothing was supplied for our team/division/league, use all teams
    if not options.team and not options.division and not options.league:
        options.team = ALLTEAMS

    # If nothing was supplied for versus team/division/league, use all teams
    if not options.versus_team and not options.versus_division and not options.versus_league:
        options.versus_team = ALLTEAMS

    # If nothing was provided for seasons, set it to 'all'
    if not options.season:
        options.season = ['all']
    else:
        try:
            _ = [int(j) for j in options.season]
        except ValueError:
            raise Exception("Error: you must provide integers to the --season flag: --season 1 --season 2")

    if options.day:
        try:
            _ = [int(j) for j in options.day]
        except ValueError:
            raise Exception("Error: you must provide integers to the --day flag: --day 86 --day 99")

    # No more user input required, so convert Dale back to utf8
    options.team = [desanitize_dale(s) for s in options.team]
    options.versus_team = [desanitize_dale(s) for s in options.versus_team]

    if options.json:
        f = JsonFormatter(options)
        f.output()
    else:
        f = TextFormatter(options)
        f.output()


def game_finder(sysargs):
    with CaptureStdout() as so:
        main(sysargs)
    return str(so)


if __name__ == '__main__':
    main()
