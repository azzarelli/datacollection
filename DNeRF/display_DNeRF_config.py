"""Rotate Cameras around Z-Axis
"""
from nerfstudio.data.dataparsers.blender_dataparser import BlenderDataParserConfig

import json
from pathlib import Path
import torch
import plotly.graph_objects as go
import numpy as np
import plotly as plt
import random as rnd
import os

##### Helper functions for later #####
def display_views_as_cones(c2w, col=0):
    """Take a set of camera exitrinsics and display the view as a cone

    Args:
        c2w: Tensor(B, 4, 4)

    Return:
        cones: go.Cone, pointing along Z-axis (for Blender data, -Z is forward direction)

    Notes:
        Plotting the quiver from the camera location in the direction the camera is pointing
    """
    if col == 0:
        cl=rnd.choice(plt.colors.DEFAULT_PLOTLY_COLORS)
    else:
        cl = plt.colors.DEFAULT_PLOTLY_COLORS[col]
    
    # Get the location of camera origin
    loc = c2w[:, :, -1]
    cam_x = loc[:, 0]
    cam_y = loc[:, 1]
    cam_z = loc[:, 2]
    
    # Project Z-axis of Camera (+Z is into View) as a Cone graph object
    rot = c2w[:, :, :3]
    back = rot[:, :, 2]  # In the 3x3 rotation matrix we take the last column representing (u, v, w) for z-axis of camera
    cones = go.Cone(x=cam_x,y=cam_y,z=cam_z, 
                    u=back[:,0], v=back[:,1], w=back[:,2],
                    colorscale=[cl,cl]
                    )
    
    # Allows you to configure the near and far ray intrinsics
    o = loc - .5*back
    cones1 = go.Cone(x=o[:,0],y=o[:,1],z=o[:,2], 
                    u=back[:,0], v=back[:,1], w=back[:,2],
                    colorscale=['red', 'red']
                    )
    
    return cones, cones1

##### Main File #####
# Define the source of our data (i.e. where we have the transform files)

def main(pth):
    source = Path(pth)
    file_type = ['train']#, 'test', 'val']

    for idx, f in enumerate(file_type):
        # Set-Up the data parser 
        dataparser_config = BlenderDataParserConfig()
        dataparser_config.data = source
        dataparser = dataparser_config.setup()

        # Parse data (for the train file - containting two cameras)
        dataparse_out = dataparser.get_dataparser_outputs(split=f)

        # Retrive camera extrinsics
        c2w = dataparse_out.cameras.camera_to_worlds
        # blue cones
        cones_original, c1 = display_views_as_cones(c2w, col=0)

        if idx == 0:
            return cones_original, c1

if __name__ == "__main__":
    fig = go.Figure()
    d1, c = main('../data/trex')
    fig.add_trace(d1)

    d2, c = main('../data/sport_dnerf')
    fig.add_trace(d2)
    fig.add_trace(c)

    fig.show()


