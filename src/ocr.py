import os
import sys
import time

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

from .database import initialize_db, save_player_pov
from .format_data import trim_name

from . import OUTPUT_ROOT_DIR


# Add your Computer Vision subscription key to your environment variables.
if "COMPUTER_VISION_SUBSCRIPTION_KEY" in os.environ:
    subscription_key = os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"]
else:
    print(
        """\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.
        **Restart your shell or IDE for changes to take effect.**"""
    )
    sys.exit()
# Add your Computer Vision endpoint to your environment variables.
if "COMPUTER_VISION_ENDPOINT" in os.environ:
    endpoint = os.environ["COMPUTER_VISION_ENDPOINT"]
else:
    print(
        """\nSet the COMPUTER_VISION_ENDPOINT environment variable.
        **Restart your shell or IDE for changes to take effect.**"""
    )
    sys.exit()

computervision_client = ComputerVisionClient(
    endpoint, CognitiveServicesCredentials(subscription_key)
)


def detect_printed_text(video_name, image_path, video_db):
    print(f"detect_printed_text for {image_path}")

    frame_nb = os.path.basename(image_path)[5:9]
    with open(image_path, "rb") as image_stream:
        recognize_printed_results = computervision_client.read_in_stream(
            image_stream, raw=True
        )

    # Get the operation location (URL with an ID at the end) from the response
    operation_location_remote = recognize_printed_results.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = operation_location_remote.split("/")[-1]

    print(f"Operation id {operation_id} for frame {frame_nb}")

    # Call the "GET" API and wait for it to retrieve the results
    while True:
        get_printed_text_results = computervision_client.get_read_result(operation_id)
        if get_printed_text_results.status not in ["notStarted", "running"]:
            break
        time.sleep(1)

    # Save detected text
    if get_printed_text_results.status == OperationStatusCodes.succeeded:
        for text_result in get_printed_text_results.analyze_result.read_results:
            if len(text_result.lines) > 0:
                line = text_result.lines[0]
                print(
                    f"Found {line.text} in frame {frame_nb} at position {line.bounding_box}"
                )
                player_name = trim_name(line.text)
                save_player_pov(video_name, player_name, frame_nb, video_db)
            else:
                print(f"No player pov in frame {frame_nb}")


def read_video_frames(video_name, video_path="", match_name=None):
    print(f"read video frames for {video_name}")

    video_db = initialize_db(match_name)

    frames_folder = os.path.join(OUTPUT_ROOT_DIR, video_path, video_name, "cropped")
    count = 0
    frames = os.listdir(frames_folder)
    for frame in frames:
        detect_printed_text(video_name, os.path.join(frames_folder, frame), video_db)
        count += 1
        print(f"{count}/{len(frames)} frames parsed")
        # Sad free tier throttling (20 requests/minute)
        # Non-free tier limits: 10 transactions per second, let's keep it chill anyway
        time.sleep(0.5)
