from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def cut_videos(input_folder, output_folder, start_time, end_time):
    for video_filename in os.listdir(input_folder):
        if video_filename.endswith(".mp4"):  # Adjust the extension if needed
            input_path = os.path.join(input_folder, video_filename)
            output_path = os.path.join(output_folder, video_filename)

            # Load video clip
            video_clip = VideoFileClip(input_path)

            # Cut video between start_time and end_time
            cut_clip = video_clip.subclip(start_time, end_time)

            # Save the cut video
            cut_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    import os

    # Set your input folder containing videos
    input_folder = "../data/plenoptic_toolbox/161029_sports1/hdVideos_old"

    # Set the output folder for the cut videos
    output_folder = "../data/161029_sports1/cut_videos"

    # Set the start and end times in seconds
    start_time = 137
    end_time = 145

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Cut videos
    cut_videos(input_folder, output_folder, start_time, end_time)