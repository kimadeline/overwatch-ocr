from .database import (
    get_frames,
    get_players,
    initialize_db,
    purge_db,
    save_player_intervals,
)


def trim_name(player_name):
    """Remove player number if any."""
    return player_name.split(" ")[-1]


def get_intervals(player, map_db_table):
    """
    Return a list of start and end intervals where the player POV was visible on-screen
    for a given map.
    Parameters: player name, and map (either a database or a table)
    """
    frames = get_frames(player, map_db_table)
    result = []

    if len(frames) == 0:
        return

    start = frames[0]
    next_frame = frames[0]

    for nb in frames[1:]:
        if int(nb) != int(next_frame) + 1:
            result.append({"start": start, "end": next_frame})
            start = nb
        next_frame = nb
    result.append({"start": start, "end": next_frame})

    return result


def get_pov_data(players, table):
    """
    Return the screen time of all players in this game in a dictionary of player handle
    keys and arrays of start/end intervals.
    """
    intervals = []

    for p in players:
        p["intervals"] = get_intervals(p, table)
        intervals.append(p)

    filtered = filter(lambda i: i["intervals"] is not None, intervals)

    return list(filtered)


def parse_player_intervals(game_map, teams):
    print(f"parse player intervals for {game_map}")
    all_players = get_players(teams)

    game_db = initialize_db("bos_was_game")
    maps_set = game_db.tables()
    maps_set.discard("_default")

    pov_db = initialize_db(f"{game_map}_pov")
    purge_db(pov_db)

    for map_name in maps_set:
        map_table = game_db.table(map_name)
        pov_data = get_pov_data(all_players, map_table)
        save_player_intervals(map_name, pov_data, pov_db)
