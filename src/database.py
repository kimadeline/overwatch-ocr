"""Databases access: read and write, occasionally sorting query results."""
import os
import re

from . import ROOT_DIR
from tinydb import TinyDB, Query

OWWC_DATABASE = os.path.join(ROOT_DIR, "data/teams.json")
GAME_DATABASE = os.path.join("data/game.json")
POV_DATABASE = os.path.join("data/pov.json")

# Read-only info about teams, players and roles
owwc_info = TinyDB(OWWC_DATABASE)

# Where to save raw game data from the OCR system
game_db = TinyDB(GAME_DATABASE)

# Where to save POV intervals data (formatted data)
pov_db = TinyDB(POV_DATABASE)


def purge_db():
    game_db.purge()


def save_player_pov(map_round, player_name, frame_nb):
    game_map = game_db.table(map_round)
    game_map.insert({"player": player_name, "frame": frame_nb})


# intervals is an array of player intervals returned by format_data.get_pov_data
def save_player_intervals(map_round, intervals):
    game_map = pov_db.table(map_round)
    game_map.insert_multiple(intervals)


def get_team(country):
    """Given a country shorthand name, gets the corresponding team object"""
    teams = owwc_info.table("teams")
    Team = Query()
    return teams.get(Team.shorthand == country)


def get_teams(countries_list):
    """Given a list of country shorthand names, gets a dictionary of team objects,
    with the keys being the shorthand names"""
    teams = owwc_info.table("teams")
    Team = Query()
    return {c: teams.get(Team.shorthand == c) for c in countries_list}


def get_player(player):
    players = owwc_info.table("players")
    Players = Query()
    return players.get(Players.name == player)


def get_players(country):
    """Given a country shorthand or a list of country shorthand names, 
    gets the players for this country."""
    players = owwc_info.table("players")
    Players = Query()
    return players.search(Players.team.one_of(country))


def get_frames(player):
    """Returns a sorted list of frame numbers in which the player POV was visible on-screen."""
    Frames = Query()
    player_frames = game_db.search(Frames.player.matches(player, flags=re.IGNORECASE))

    return sorted([f["frame"] for f in player_frames])
