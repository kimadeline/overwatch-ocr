import os

GAMES_LIST = [
    "illios",
    "dorado_round_1",
    "dorado_round_2",
    "kings_row_round_1",
    "kings_row_round_2",
]

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(ROOT_DIR, "input")
OUTPUT_ROOT_DIR = os.path.join(ROOT_DIR, "output")
