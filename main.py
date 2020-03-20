from src import GAMES_LIST
from src.crop import crop_video_frames
from src.format_data import parse_player_intervals
from src.ocr import read_video_frames
from src.parse import split_video_frames
from src.plot import display_dashboard

# split and crop
for game_map in GAMES_LIST:
    print(f"----- START LOCAL VIDEO PARSING OF {game_map} -----")
    filename = f"{game_map}.mp4"
    # split frames
    split_video_frames(filename)
    # crop player name
    crop_video_frames(game_map)
    # send them to OCR
    read_video_frames(game_map)
    # parse intervals and save them to DB
    parse_player_intervals(game_map)
    print(f"----- END LOCAL VIDEO PARSING OF {game_map} -----")

display_dashboard()
