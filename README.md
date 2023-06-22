# Turn your Nerfstudio data into DNeRF data with the original video and the nerfstudio processed dataset

All background and instructions are provided in `nstudio2dnerf.ipynb`.

You will need to set the notebook kernel to use the nerfstudio conda environment. No additional dependencies are needed. GPU isn't used

TODO:
    Use GPU to speed up SSIM comparison (pytorch?) or cv2.cuda (though the second option requires additional binaries which I and other may not have installed)