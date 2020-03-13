import plotly.graph_objects as go
import json

from collections import defaultdict


stats = {"teams": defaultdict(int), "roles": defaultdict(int)}


def team_colors(team):
    if team == "USA":
        return "blue"
    elif team == "CHN":
        return "red"
    else:  # This shouldn't happen
        return "black"


def role_colors(role):
    if role == "Tank":
        return "Goldenrod"
    elif role == "Damage":
        return "HotPink"
    elif role == "Support":
        return "LimeGreen"
    else:  # This shouldn't happen
        return "black"


def team_datapoints(player_data):
    datapoints = {"x": [], "y": [], "text": [], "color": []}
    for interval in player_data["intervals"]:
        start = int(interval["start"])
        end = int(interval["end"]) + 1
        for frame in range(start, end):
            datapoints["x"].append(frame)
            datapoints["y"].append(1)
            datapoints["text"].append(f"{player_data['name']}<br>{player_data['role']}")
            datapoints["color"].append(team_colors(player_data["team"]))
            add_team_stats(player_data["team"])
            add_role_stats(player_data["role"])
    return datapoints


def role_datapoints(player_data):
    datapoints = {"x": [], "y": [], "text": [], "color": []}
    for interval in player_data["intervals"]:
        start = int(interval["start"])
        end = int(interval["end"]) + 1
        for frame in range(start, end):
            datapoints["x"].append(frame)
            datapoints["y"].append(1)
            datapoints["text"].append(f"{player_data['name']}<br>{player_data['team']}")
            datapoints["color"].append(role_colors(player_data["role"]))
            add_team_stats(player_data["team"])
            add_role_stats(player_data["role"])
    return datapoints


# team parameter = player_data["team"]
def add_team_stats(team):
    stats["teams"][team] += 1


# role parameter = player_data["role"]
def add_role_stats(role):
    stats["roles"][role] += 1


# USA / CHN
def compute_team_stats(team1, team2):
    total = sum(stats["teams"].values())

    team1_percentage = stats["teams"][team1] / total * 100
    team2_percentage = stats["teams"][team2] / total * 100

    return {team1: team1_percentage, team2: team2_percentage}


def compute_role_stats():
    total = sum(stats["roles"].values())
    result = {}
    for key, value in stats["roles"].items():
        result[key] = value / total * 100

    return result


# type is either "TEAM" (team comparison red vs blue)
# or "ROLE" (role comparison)
def display_single_plot(type):
    with open("data/_pov_data.json") as p:
        pov_data = json.load(p)

    x = []
    y = []
    text = []
    color = []
    for player in pov_data:
        player_datapoints = (
            role_datapoints(player) if type == "ROLE" else team_datapoints(player)
        )
        x += player_datapoints["x"]
        y += player_datapoints["y"]
        text += player_datapoints["text"]
        color += player_datapoints["color"]

    fig = go.Figure(
        data=go.Scatter(
            x=x,
            y=y,
            mode="markers",
            text=text,
            marker={"symbol": "square", "color": color},
        )
    )
    fig.show()


if __name__ == "__main__":
    display_single_plot("ROLE")

    team_stats = compute_team_stats("USA", "CHN")
    role_stats = compute_role_stats()
    print(f"team stats: {team_stats} - role stats: {role_stats}")
