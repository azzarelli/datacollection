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
    back = rot[:, :, 2] # In the 3x3 rotation matrix we take the last column representing (u, v, w) for z-axis of camera
    cones = go.Cone(x=cam_x,y=cam_y,z=cam_z, 
                    u=back[:,0], v=back[:,1], w=back[:,2],
                    colorscale=[cl,cl]
                    )

    return cones

##### Main File #####
# Define the source of our data (i.e. where we have the transform files)

def main():
    source = Path('./data/sport_dnerf')
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
        cones_original = display_views_as_cones(c2w, col=1)

        if idx == 0:
            # Plot our cones + Z-Axis + World origin
            zaxis_line = go.Scatter3d(x=[0, 0],y=[0,0],z=[-0, 5],line=dict(
                    color='darkblue',
                    width=2
                ))
            yaxis_line = go.Scatter3d(x=[0, 0],y=[0,5],z=[-0, 0],line=dict(
                    color='red',
                    width=2
                ))
            xaxis_line = go.Scatter3d(x=[0, 5],y=[0,0],z=[-0, 0],line=dict(
                    color='green',
                    width=2
                ))

            from plotly import offline
            
            fig = go.Figure() #data=[cones_original, zaxis_line, yaxis_line, xaxis_line])
            fig.add_trace(cones_original)
            offline.plot(fig) # instead of fig.show()


            fig.show()



if __name__ == "__main__":
    main()

