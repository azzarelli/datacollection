import cv2
import os

def extract_frames(video_path, output_folder, id):
    # Create output folder if not exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Unable to open video.")
        return

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Loop through each frame and save it as an image
    for frame_number in range(total_frames):
        # Read a single frame from the video
        ret, frame = cap.read()
        
        # Check if frame was successfully read
        if not ret:
            print(f"Error: Unable to read frame {frame_number}.")
            break

        # Save the frame as an image
        frame_name = f"{id:04d}.png"
        frame_path = os.path.join(output_folder, frame_name)
        cv2.imwrite(frame_path, frame)

    # Release the video capture object
    cap.release()
    print(f"Frames extracted successfully from {video_path} to {output_folder}.")

if __name__ == "__main__":
    # Specify the path to the folder containing videos
    video_folder = "../data/plenoptic_toolbox/161029_sports1/llff"
    
    # Specify the path to the folder where frames will be saved
    output_folder = "../outputs"

    # Iterate through each video file in the folder
    for i, video_file in enumerate(os.listdir(video_folder)):
        video_path = os.path.join(video_folder, video_file)
        
        # Check if the file is a video (you can add more specific checks here if needed)
        if video_file.endswith((".mp4", ".avi", ".mkv")):
            # Create a folder for each video to save frames
            video_name = os.path.splitext(video_file)[0]
            video_output_folder = os.path.join(output_folder, video_name)
            extract_frames(video_path, video_output_folder, i)
