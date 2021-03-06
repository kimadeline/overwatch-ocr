"""Databases access: read and write, occasionally sorting query results."""
import os
import re

from . import ROOT_DIR
from tinydb import TinyDB, Query

TEAM_DATABASE = os.path.join(ROOT_DIR, "data/teams.json")
GAME_DATABASE = os.path.join("data/game.json")
POV_DATABASE = os.path.join("data/pov.json")

# Read-only info about teams, players and roles
team_info = TinyDB(TEAM_DATABASE)

# Where to save raw game data from the OCR system
game_db = TinyDB(GAME_DATABASE)

# Where to save POV intervals data (formatted data)
pov_db = TinyDB(POV_DATABASE)


def purge_db(db_name=game_db):
    db_name.drop_tables()

    return db_name


def initialize_db(video_name):
    if video_name:
        db_path = os.path.join("data", f"{video_name}.json")
        video_db = TinyDB(db_path)
    else:
        video_db = game_db
    return video_db


def save_player_pov(map_round, player_name, frame_nb, video_db=game_db):
    game_map = video_db.table(map_round)
    game_map.insert({"player": player_name, "frame": frame_nb})


# intervals is an array of player intervals returned by format_data.get_pov_data
def save_player_intervals(map_round, intervals, database=pov_db):
    game_map = database.table(map_round)
    game_map.insert_multiple(intervals)


def get_team(shorthand):
    """Given a team shorthand name, gets the corresponding team object."""
    teams = team_info.table("teams")
    Team = Query()
    return teams.get(Team.shorthand == shorthand)


def get_teams(teams_list):
    """
    Given a list of team shorthand names, gets a dictionary of team objects,
    with the keys being the shorthand names.
    """
    teams = team_info.table("teams")
    Team = Query()
    return {t: teams.get(Team.shorthand == t) for t in teams_list}


def get_player(player):
    players = team_info.table("players")
    Players = Query()
    return players.get(Players.name == player)


def get_players(teams_list):
    """Given a list of team shorthand names,
    returns the players for all teams in one big list."""

    teams = team_info.table("teams")
    Team = Query()
    result = []

    for t in teams_list:
        roles = teams.get(Team.shorthand == t)["players"]
        result += [{"name": p, "role": "damage", "team": t} for p in roles["damage"]]
        result += [{"name": p, "role": "tank", "team": t} for p in roles["tank"]]
        result += [{"name": p, "role": "support", "team": t} for p in roles["support"]]

    return result


def get_frames(player, table=game_db):
    """Returns a sorted list of frame numbers
    in which the player POV was visible on-screen."""
    Frames = Query()
    player_frames = table.search(
        Frames.player.matches(player["name"], flags=re.IGNORECASE)
    )

    return sorted([f["frame"] for f in player_frames])
