
import json
import os

from . import FOLDERS, ROOT_DIR

from collections import defaultdict

games_list = []
for games in FOLDERS.values():
    games_list.extend(games)

# It should look like this:
#
# games_list = [
#     "hou_bos_w10_maps",
#     "hzs_cdh_w10_maps",
#     "phi_par_w10_maps",
#     "van_gzc_w10_maps",
#     "was_dal_w10_maps",
#     "cdh_van_w10_maps",
#     "hou_tor_w10_maps",
#     "phi_atl_w10_maps",
#     "sfs_gla_w10_maps",
#     "shd_gzc_w10_maps",
# ]

# What is happening here:
#
# for each game:
#     extract teams
#     load json
#     for each map:
#         compute role stats
#         compute team stats
#     add to total stats
#     save that somewhere


def add_team_stats(team, count, stats):
    stats[team] += count
    return stats


# role parameter = player_data["role"]
def add_role_stats(role, count, stats):
    stats[role] += count
    return stats


def iterate_player_data(map_players):
    stats = {"teams": defaultdict(int), "roles": { "tank": 0, "damage": 0, "support": 0}}

    for player_data in map_players.values():
        for interval in player_data["intervals"]: 
            start = int(interval["start"])
            end = int(interval["end"]) + 1

            add_team_stats(player_data["team"], end - start, stats["teams"])
            add_role_stats(player_data["role"], end - start, stats["roles"])
    
    return stats

def compute_team_stats(team1, team2, stats = defaultdict(int)):
    total = sum(stats["teams"].values())

    team1_percentage = stats["teams"][team1] / total * 100
    team2_percentage = stats["teams"][team2] / total * 100

    return {team1: round(team1_percentage, 2), team2: round(team2_percentage, 2)}


def compute_role_stats(stats = defaultdict(int)):
    total = sum(stats["roles"].values())
    result = {}
    for key, value in stats["roles"].items():
        result[key] = round(value / total * 100, 2)

    return result

def compute_stats():
    output_file = os.path.join(ROOT_DIR, "data/owl_stats.json")
    output_dict = {}

    for game in games_list:
        output_dict[game] = {}
        
        teams = [t.upper() for t in game.split("_")[:2]] # [ HOU, BOS ]
        first = teams[0]
        second = teams[1]

        pov_json_filename = os.path.join(ROOT_DIR, f"data/{game}_pov.json")

        with open(pov_json_filename) as p:
            pov_data = json.load(p)
            game_stats = {"teams": { first: 0, second: 0}, "roles": { "tank": 0, "damage": 0, "support": 0}}

            map_count = 0
            for map_name, player_data in pov_data.items():
                if map_name != "_default":
                    stats = iterate_player_data(player_data)
                    map_stats = {
                        "teams": compute_team_stats(first, second, stats),
                        "roles": compute_role_stats(stats)
                    }                    

                    game_stats["teams"][first] += map_stats["teams"][first]
                    game_stats["teams"][second] += map_stats["teams"][second]
                    game_stats["roles"]["tank"] += map_stats["roles"]["tank"]
                    game_stats["roles"]["damage"] += map_stats["roles"]["damage"]
                    game_stats["roles"]["support"] += map_stats["roles"]["support"]

                    output_dict[game][map_name] = map_stats
                    map_count += 1

            game_stats["teams"][first] = round(game_stats["teams"][first] / map_count, 2)
            game_stats["teams"][second] = round(game_stats["teams"][second] / map_count, 2)
            game_stats["roles"]["tank"] = round(game_stats["roles"]["tank"] / map_count, 2)
            game_stats["roles"]["damage"] = round(game_stats["roles"]["damage"] / map_count, 2)
            game_stats["roles"]["support"] = round(game_stats["roles"]["support"] / map_count, 2)

            output_dict[game]["total"] = game_stats
                

    with open(output_file, 'w') as outfile:
        json.dump(output_dict, outfile)
    
    print("the end")

compute_stats()

