# Helpful python programs for video data processing
I primarily use this to preprocess video data for dynamic NeRF models.

## Nerfstudio to DNeRF data  (Python Notebook)
All background and instructions are provided in `nstudio2dnerf.ipynb`. You may want to customise the `camera_angle_x` parameter which sets the focal lengths of the camera models

I have tested the `linear` method and are working on the `exhaustive` method. 

Models:
1. [k-planes nerfstudio](https://github.com/Giodiro/kplanes_nerfstudio) - works
2. [d-nerf](https://github.com/albertpumarola/D-NeRF/tree/main) - could not implement (requires cuda 10.2)

## Video to Image Extraction (Python)
I took and minorly modified a script from [Geeks4Geeks](https://www.geeksforgeeks.org/extract-images-from-video-in-python/) (minor modifications) to extract images for [RoDynRF](https://github.com/facebookresearch/robust-dynrf)

## Sync-Cut Two Videos using Tk GUI
Rudimentary implementation of a Tk GUI which allows us to select the start point (sync reference and start frame) and cut point (end frame).
This script allow you to sync two videos by cutting each video by selecting the start frame of each video and end frame of the chosen video. Then, it cuts both videos to start at the desired frames and last the same amount of time.

You can directly modify the script `sync_two_videos.py` to select a `path` to a folder containing the two videos `f1` and `f2`. 

After running the script you'll be presented with a Tk GUI. Follow the steps below to sync the videos

1. `-100, -10, -1, +1, +10, +100` : Select the sync frame for each video (I used a clip-board)
2. `cut start` : After selecting the sync frame, press this button for both videos. 
3. `-100, -10, -1, +1, +10, +100` : Select a new frame **for one video**
4. `cut end` : After selecting the end frame for you chosen video, press this button to cut both videos
5. Wait a min... (we dont copy our video as it has unsuported codec so its going to be slow)
5. Check `$PATH/ouputs/` to see the processed videos
