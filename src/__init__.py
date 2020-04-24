import os

FOLDERS = {
    "owl_w10_d1": [
        "hou_bos_w10_maps",
        "hzs_cdh_w10_maps",
        "phi_par_w10_maps",
        "van_gzc_w10_maps",
        "was_dal_w10_maps",
    ],
    "owl_w10_d2": [
        "cdh_van_w10_maps",
        "hou_tor_w10_maps",
        "phi_atl_w10_maps",
        "sfs_gla_w10_maps",
        "shd_gzc_w10_maps",
    ],
}

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
