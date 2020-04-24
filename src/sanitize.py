import os
import re

from . import ROOT_DIR
from tinydb import TinyDB, Query

OWL_DATABASE = os.path.join(ROOT_DIR, "data/teams.json")

# Read-only info about teams, players and misspellings
owl_info = TinyDB(OWL_DATABASE)
teams = owl_info.table("teams")


def sanitize_names(match_name, teams_shorthands):
    match_db_path = os.path.join(ROOT_DIR, "data", f"{match_name}.json")
    match_db = TinyDB(match_db_path)

    maps_set = match_db.tables()
    maps_set.discard("_default")

    for map_name in maps_set:
        map_table = match_db.table(map_name)

        for shorthand in teams_shorthands:
            print(f"Sanitize names for {shorthand} in {map_name}")
            Team = Query()
            team = teams.get(Team.shorthand == shorthand.upper())

            for player_name, variants in team["misspellings"].items():
                Map = Query()
                map_table.update(
                    {"player": player_name.upper()}, Map.player.one_of(variants)
                )


# Example use
# sanitize_names("bos_was_w5_maps", ["bos", "was"])

sanitize_names("hou_bos_w10_maps", ["hou", "bos"])
sanitize_names("hzs_cdh_w10_maps", ["hzs", "cdh"])
sanitize_names("phi_par_w10_maps", ["phi", "par"])
sanitize_names("van_gzc_w10_maps", ["van", "gzc"])
sanitize_names("was_dal_w10_maps", ["was", "dal"])

sanitize_names("cdh_van_w10_maps", ["cdh", "van"])
sanitize_names("hou_tor_w10_maps", ["hou", "tor"])
sanitize_names("phi_atl_w10_maps", ["phi", "atl"])
sanitize_names("sfs_gla_w10_maps", ["sfs", "gla"])
sanitize_names("shd_gzc_w10_maps", ["shd", "gzc"])
