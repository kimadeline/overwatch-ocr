# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

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
    if role.lower() == "tank":
        return "Goldenrod"
    elif role.lower() == "damage":
        return "HotPink"
    elif role.lower() == "support":
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
    return datapoints


# team parameter = player_data["team"]
def add_team_stats(team, count=1):
    stats["teams"][team] += count


# role parameter = player_data["role"]
def add_role_stats(role, count=1):
    stats["roles"][role] += count


def compute_game_stats(pov_data):
    for player_data in pov_data:
        for interval in player_data["intervals"]:
            start = int(interval["start"])
            end = int(interval["end"]) + 1
            add_team_stats(player_data["team"], end - start)
            add_role_stats(player_data["role"], end - start)


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
def get_datapoints(pov_data, type):
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

    return {"x": x, "y": y, "text": text, "color": color}


def start_dashboard_server(pov_data, team_stats, role_stats, game_name, map_name):
    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    role_points = get_datapoints(pov_data, "ROLE")
    team_points = get_datapoints(pov_data, "TEAM")

    app.layout = html.Div(
        children=[
            html.H2(children=f"Game: {game_name} - {map_name}"),
            html.Div(children=f"team stats: {team_stats} - role stats: {role_stats}"),
            dcc.Graph(
                id="role-graph",
                figure={
                    "data": [
                        go.Scatter(
                            x=role_points["x"],
                            y=role_points["y"],
                            mode="markers",
                            text=role_points["text"],
                            marker={"symbol": "square", "color": role_points["color"]},
                        )
                    ],
                    "layout": {"title": "Role distribution"},
                },
            ),
            dcc.Graph(
                id="team-graph",
                figure={
                    "data": [
                        go.Scatter(
                            x=team_points["x"],
                            y=team_points["y"],
                            mode="markers",
                            text=team_points["text"],
                            marker={"symbol": "square", "color": team_points["color"]},
                        )
                    ],
                    "layout": {"title": "Team distribution"},
                },
            ),
        ]
    )

    app.run_server(debug=True)


# Datapoint keys: x, y, text and color
def generate_graph(datapoints):
    fig = go.Figure(
        data=go.Scatter(
            x=datapoints.x,
            y=datapoints.y,
            mode="markers",
            text=datapoints.text,
            marker={"symbol": "square", "color": datapoints.color},
        )
    )

    return fig


def display_graph(filepath="data/pov_data.json"):
    with open(filepath) as p:
        pov_data = json.load(p)

    compute_game_stats(pov_data)
    team_stats = compute_team_stats("USA", "CHN")
    role_stats = compute_role_stats()

    datapoints = get_datapoints(pov_data, "ROLE")
    figure = generate_graph(datapoints)
    print(f"team stats: {team_stats} - role stats: {role_stats}")
    figure.show()


def display_dashboard(filepath="data/pov_data.json"):
    with open(filepath) as p:
        pov_data = json.load(p)

    compute_game_stats(pov_data)
    team_stats = compute_team_stats("USA", "CHN")
    role_stats = compute_role_stats()

    start_dashboard_server(
        pov_data, team_stats, role_stats, "USA vs China - OWWC 2019", "all maps"
    )
