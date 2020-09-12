# blaseball-game-finder

This repo contains a command line tool called `game-finder`
that helps find game IDs of blaseball games. This is a utility
function to make other tools easier to use.

You can use command line flags or configuration options to filter
on conditions, including:

* Season
* Day
* Team (home, away, either)
* Opponent
* Postseason


## Table of Contents

* [Screenshots](#screenshots)
* [Installation](#installation)
    * [pip](#pip)
    * [source](#source)
* [Quick Start](#quick-start)
    * [Command line flags](#command-line-flags)
    * [Configuration file](#configuration-file)
* [Data](#data)
* [Configuration Examples](#configuration-examples)
* [Software architecture](#software-architecture)
* [Who is this tool for?](#who-is-this-tool-for)
* [Future work](#future-work)
    * [Libraries used](#libraries-used)


## Output Formats

The blaseball-game-finder can output data in text format or json format.

The text format consists of game ID only, one game ID per line of output,
printed to stdout. This is ideal for building pipes on the command line.

The json format consists of game ID, along with several other fields.
(??)

## Installation

### pip

```
pip install blaseball-game-finder
```

### source

Start by cloning the package:

```
git clone https://github.com/ch4zm/blaseball-game-finder
cd blaseball-game-finder
```

If installing from source, it is recommended you install the package
into a virtual environment. For example:

```
virtualenv vp
source vp/bin/activate
```

Now build and install the package:

```
python setup.py build
python setup.py install
```

Now test that the tool is available on the command line, and try out
a command to search for some games:

```
which game-finder
game-finder --season 4 --game 20 --team Sunbeams
```

## Quick Start

The way this tool works is, it creates a data frame object, applies some filters to it based on command line flags provided
by the user, then runs the data frame through a data viewer (which makes the nice tables). All command line flags can also 
be specified in a config file.

### Command line flags

Command line flags are grouped into data options and format options.

Data options:

* **Season**: Set season for game data using `--season`. For multiple seasons, repeat the flag: `--season 1 --season 2`

* (Optional) **Our Team**: Specify only one of the following:
    * **Team**: use the `--team` flag to specify the short name of your team (use `--help` to see
      valid choices). For multiple teams, use multiple `--team` flags.
    * **Division**: use the `--division` flag to specify the name of a division. Surround division
      name in quotes, e.g., `--division "Lawful Evil"`
    * **League**: use the `--league` flag to specify the Good/Evil league

* (Optional) **Versus Team**: Specify only one of the following:
    * **Versus Team**: use the `--versus-team` flag to specify the short name of the opposing team (use `--help` to see
      valid choices). For multiple teams, use multiple `--versus-team` flags.
    * **Versus Division**: use the `--versus-division` flag to specify the name of the versus division. Surround division
      name in quotes, e.g., `--versus-division "Lawful Evil"`
    * **Versus League**: use the `--versus-league` flag to specify the versus Good/Evil league

(If neither flag is specified, it will include all games between all teams.)

Format options:

* **JSON**: Use `--json` to specify that the output should be in JSON format.
  This will include details about each game (see above).

* **Text**: (Default choice) Use `--text` to output game IDs as plain text,
  one game ID per line, with no additional information.

Using a configuration file:

* **Config file**: use the `-c` or `--config` file to point to a configuration file (see next section).


######################################################################################
######################################################################################
######################################################################################
##################   i stopped here    ###############################################
######################################################################################
######################################################################################
######################################################################################





### Configuration file

(Note: several configuration file examples are provided in a section below.)

Every command line flag can be specified in a configuration file as well.
To reproduce the following command line call,

```
game-finder --season 1 --season 2 --team Tigers --versus-team Pies --text
```

we could create a configuration file named `config.ini` with the contents:

```
season = [1, 2]
team = Tigers
versus-team = Pies
text
```

and run `blaseball-game-finder` specifying that configuration file:

```
game-finder --config config.ini
# or
game-finder -c config.ini
```

This would produce identical output to the command with all the flags.

You can also use both a config file and command line flags; the command line flags will take
precedence over config file options if a parameter is specified by both.


## Data

The data set used by this tool comes from `blaseball.com`'s `/games` API endpoint.
The data set is imported from [`blaseball-core-game-data`](https://githib.com/ch4zm/blaseball-core-game-data).


## Configuration Examples

See [`config.example.ini`](https://github.com/ch4zm/blaseball-game-finder/tree/master/config.example.ini)
in the repo for an example config file.

Show game IDs from season 3 and season 4 for all games involving the Hades Tigers:

```
[data]
season = [3, 4]
team = Tigers

[format]
text
```

Include games involving the Pies too:

```
[data]
season = [3, 4]
team = [Tigers, Pies]

[format]
text
```

Include games only involving _both_ the Tigers and the Pies:

```
[data]
season = [3, 4]
team = Tigers
versus-team = Pies

[format]
text
```

Show game IDs from season 1 for all teams in the Good League:

```
[data]
season = 1
league = Good

[format]
text
```

Show game IDs for all postseason games:

```
[data]
postseason

[format]
text
```

Show the same game IDs but in JSON format:

```
[data]
postseason

[format]
json
```

## Software architecture

This software consists of three parts:

* The command line flag and config file parser (uses `configargparse` library) - see `cli/command.py`
* The BaseFormat object that provides a formatting layer to print out the JSON data in either
  plain text format (one game ID per line) or in JSON format (reduced set of information from the
  original JSON). All filtering is performed using list comprehensions, so that a data soting tool
  like pandas is not needed.


## Who is this tool for?

This tool is for the blaseball community. It will be useful to people
interested in exploring game data, people who are brainstorming about
lore for their team, and people who are looking for a starting point
for developing their own blaseball tool.


## Future work

* Add weather


## Libraries used

This command line tool uses the following libraries under the hood:

* [blaseball-core-game-data](https://github.com/ch4zm/blaseball-core-game-data)
* [configarparse](https://github.com/bw2/ConfigArgParse) for handling CLI arguments
