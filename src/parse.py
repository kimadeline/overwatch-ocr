# input -> a video
# output -> list of frames in the output folder

import logging
import os

import ffmpeg

from . import INPUT_DIR, OUTPUT_ROOT_DIR, ROOT_DIR

logging.basicConfig(level=logging.INFO)


def split_video_frames(video_name, video_path=""):
    print(f"split video frames for {video_name}")
    output_dir = os.path.join(
        OUTPUT_ROOT_DIR, video_path, video_name.rpartition(".")[0], "frames"
    )

    logging.info(f"input_dir: {INPUT_DIR}")
    logging.info(f"output_dir: {output_dir}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    in_filename = os.path.join(INPUT_DIR, video_path, video_name)
    out_filename = os.path.join(output_dir, "frame%04d.png")
    # r=X frames per second
    ffmpeg.input(in_filename).output(out_filename, r=1).run()
