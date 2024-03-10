# Handy-Dany python programs for Processing NeRF datasets
Some handy scripts for transforming/editing datasets (python & notebook). These are mainly used for modifying NeRF research datasets - for research purposes. 

Explanations are also provided alongside the relevant tasks so even if the programs aren't relevant hopefully the explanations may be useful.

*Note: Number of bugs may be present from moving files around and not correcting hierarchy*

## Contents
- `video_editing` contains scripts for editing mp4 video files
- `DNeRF/` contains D-NeRF specific scripts
- `NeRF2DNeRF` contains scripts for converting nerfstudio generated scripts to D-NeRF format
- `PTB2DNeRF` contains scripts for converting the PlenopticToolBox dataset to D-NeRF format
- `misc` contains a script to elongate a D-NeRF dataset by making it a boomerang video.

### Notes
The code is written for research-purposes only. The relecant Licenses (mainly for nerfstudio) are provided. Otherwise, the othr scripts are not considered licensed.

None of the scripts delet existing work - however some of them will over-write prior runs so just be aware of his before running!

I am not a software engineer so feedback/edits are very welcome :))))

## Video Editing

#### `.../cut_multiview_videos.py`
Uses [moviepy](https://pypi.org/project/moviepy/) python library to cut a set of videos (videos expected to be in-sync). Requires [ffmpeg](https://www.ffmpeg.org/download.html).

#### `.../sync_two_videos.py`
Usese `PIL` and `opencv` to create a TK gui for manually syncing multiple videos. This script allow you to sync two videos by cutting each video by selecting the start frame of each video and end frame of the chosen video. Then, it cuts both videos to start at the desired frames and last the same amount of time.

You can directly modify the script `sync_two_videos.py` to select a `path` to a folder containing the two videos `f1` and `f2`. 

After running the script you'll be presented with a Tk GUI. Follow the steps below to sync the videos

1. `-100, -10, -1, +1, +10, +100` : Select the sync frame for each video (I used a clip-board)
2. `cut start` : After selecting the sync frame, press this button for both videos. 
3. `-100, -10, -1, +1, +10, +100` : Select a new frame **for one video**
4. `cut end` : After selecting the end frame for you chosen video, press this button to cut both videos
5. Wait a min... (we dont copy our video as it has unsuported codec so its going to be slow)
5. Check `$PATH/ouputs/` to see the processed videos

#### `.../video_to_jpg.py`
I took and minorly modified a script from [Geeks4Geeks](https://www.geeksforgeeks.org/extract-images-from-video-in-python/) (minor modifications) to extract images for [RoDynRF](https://github.com/facebookresearch/robust-dynrf)

## DNeRF

#### `.../add_noise_to_dnerf.py`
Uses `PIL` and `opencv` to add guassian noise to dnerf image dataset.

#### `.../display_DNeRF_config.py`

Displays D-NeRF training dataset using [plotly GO](https://plotly.com/python/graph-objects/). Requires the [nerfstudio](https://docs.nerf.studio/) library as it uses the Blender data parser

See `PTB2DNeRF/pelonptictoolbox_visualise.ipynb` for displaying the D-NeRF dataset with `matplotlib` and without requiring `nerfstudio`

#### `.../dnerf_blender_views.py`

A Blender Python API script for generating data for a two camera set-up.

#### `.../rotate_blender_data.py`

Rotates the D-NeRF data set given a inputs in degrees. Requires the [nerfstudio](https://docs.nerf.studio/) library as it uses the Blender data parser and is visualised using [plotly GO](https://plotly.com/python/graph-objects/).

See `PTB2DNeRF/pelonptictoolbox_visualise.ipynb` for an implementation that doesn't requirethe `nerstudio` library.

#### `.../transforms_to_train_test_val.py`

Converts a folder containing a single `transform.json` file into a folder containing the training, test and validation split. Manages folders for the relevant split.

## NeRF2DNeRF

#### `.../nstudio2dnerf.ipynb`
All background and instructions are provided in `nstudio2dnerf.ipynb`. You may want to customise the `camera_angle_x` parameter which sets the focal lengths of the camera models

The `linear` and `exhaustive` methods work towards seperate goals. 

The `exhaustive` method tries to match images to their corresponding frame in a video sequence, thus infer the relevant time frame. This is useful for data sets where time is not infered from the image/name. This only works with datasets that use the `camera_angle_x` parameter (i.e. original D-NeRF format).

The `linear` method uses the `file_path` key for the original dataset to infer the time-frame of an image in the video sequence. I.e. an image named `.../frame_200.png` will be the 200th time frame in the sequence. This methods works with datasets containing the `camera_angle_x` parameter OR datasets where the `fl_x, fl_y, ...` parameters are avaliable (these are usually present in nerfstudio/colmap data sets).

## PTB2DNeRF

#### `.../pelonptictoolbox_visualise.ipynb`
This allows you to configure and visuale the PTB dataset using an existing D-NeRF dataset to compare.

As the PTB dataset is not scaled or rotated correctly, this file will allow us to rotate and scale correctly. Using the D-NeRF dataset for comparison will help us scale and rotate.

You may want to note down the x,y,z limits for you dataset as this will tell you what the limits should be on you scene AABB model.

#### `.../pelonptictoolbox2DNeRF.ipynb`
This is a more manual approach to the above notebook without rotation correction and without comparison. You can replace the `fl_x, fl_y ...` with your own intrinsics

