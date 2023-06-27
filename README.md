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

