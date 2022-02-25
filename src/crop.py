import os

from PIL import Image

from . import OUTPUT_ROOT_DIR

# Image should be at least 50x50
PLAYER_NAME_AREA = (
    187,
    550,
    315,
    600,
)  # top left x, top left y, bottom right x, bottom right y


def crop_player_name(image_path, dest_folder):
    """Adding a comment for a PR.
    """
    image_fullname = os.path.basename(image_path)
    image = Image.open(image_path)

    player_name = image.crop(PLAYER_NAME_AREA)

    image_name = image_fullname.rpartition(".")[0]
    filename = os.path.join(dest_folder, f"{image_name}_player.png")
    player_name.save(filename)
    print(f"Cropped the player name for {image_name}")


def crop_video_frames(video_name, video_path=""):
    print(f"crop video frames for {video_path}/{video_name}")
    frames_folder = os.path.join(OUTPUT_ROOT_DIR, video_path, video_name, "frames")
    dest_folder = os.path.join(OUTPUT_ROOT_DIR, video_path, video_name, "cropped")

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    frames = os.listdir(frames_folder)
    for frame in frames:
        crop_player_name(os.path.join(frames_folder, frame), dest_folder)
