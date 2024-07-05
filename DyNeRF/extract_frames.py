import cv2
import os
import threading
from queue import Queue

# Modified my Chatgpt output - lol

def extract_frames(video_path, output_folder, num_threads=4):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

        # Capture the video
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return

    # Frame counter
    frame_number = 0

    while True:
        # Read a frame
        ret, frame = cap.read()

        # If no frame is returned, end of video
        if not ret:
            break

        # Construct the output frame path
        frame_path = os.path.join(output_folder, f"{frame_number:04d}.png")

        # Save the frame as an image file
        cv2.imwrite(frame_path, frame)

        # Increment the frame counter
        frame_number += 1

    # Release the video capture object
    cap.release()
    print(f"Extracted {frame_number} frames to {output_folder}")


# Example usage
path = '/home/xi22005/DATA/dynerf/flame_steak/'

videos = os.listdir(path)

frame_dirs = []
video_dirs = []
for video in videos:
    cam_path = path + video.split('.')[0]

    video_dirs.append(path+video)
    frame_dirs.append(cam_path)

for video, output in zip(video_dirs, frame_dirs):
    if 'cam00' in video:
        print(f'Extracting frames from {video}')
        extract_frames(video, output)
# extract_frames(video_path, output_folder)
