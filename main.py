import os

from src import FOLDERS, INPUT_DIR
from src.crop import crop_video_frames
from src.format_data import parse_player_intervals
from src.ocr import read_video_frames
from src.parse import split_video_frames
from src.plot import display_dashboard

for week, matches in FOLDERS.items():
    for match in matches:
        print(f"----- FETCH VIDEOS IN {week}/{match} -----")
        folder = os.path.join(INPUT_DIR, week, match)
        videos = os.listdir(folder)
        for video in videos:
            if not video.endswith(".DS_Store"):
                video_path = os.path.join(week, match)
                video_name = video[:-4]
                print(
                    f"----- START LOCAL VIDEO PARSING OF {week}/{match}/{video} -----"
                )
                # split frames
                split_video_frames(video, video_path)
                # crop player name
                crop_video_frames(video_name, video_path)
                # send them to OCR
                read_video_frames(video_name, video_path, match)
                print(f"----- END LOCAL VIDEO PARSING OF {week}/{match}/{video} -----")

for week, matches in FOLDERS.items():
    for match in matches:
        print(f"----- START PARSING OF PLAYER INTERVALS FOR {week}/{match} -----")
        components = match.split("_")
        teams = [c.upper() for c in components[:2]]
        parse_player_intervals(match, teams)
        print(f"----- END PARSING OF PLAYER INTERVALS FOR {week}/{match} -----")

display_dashboard()
