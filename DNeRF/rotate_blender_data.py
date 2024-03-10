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

def write_extrinsics(c2w, source, f, name='newtransforms'):
    """ Taking new extrinsics matrix replace old extrinsics (write new files)
    """
    src = source / f"transforms_{f}.json"
    print(src)
    with open(src) as fp:
        contents = fp.read()
    meta = json.loads(contents)

    frames = meta['frames']

    frames_ = []
    for frame, extr in zip(frames, c2w):
        frame_ = frame.copy()
        extr[-1, -1] = 1.

        frame_["transform_matrix"] = extr.tolist()
        # frame_["transform_matrix"].append([0., 0., 0., 1.])

        frames_.append(frame_)

    meta['frames'] = frames_
    
    if not os.path.isdir(source/f'{name}/'):
        os.mkdir(source/f'{name}/')

    json_object = json.dumps(meta, indent=4)
    with open(source / f"{name}/transforms_{f}.json", "w") as outfile:
        outfile.write(json_object)

##### Main File #####
# Define the source of our data (i.e. where we have the transform files)

def main(angx, angz, angy):
    source = Path('./data/plenoptic_toolbox/161029_sports1/dnerf/')
    file_type = ['train', 'test', 'val']
    name = f'rotated_{angx}_{angy}_{angz}'

    # Convert deg to radians
    angz = angz * np.pi / 180.
    angx = angx * np.pi / 180
    angy = angy * np.pi / 180


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

        # Transform extrinsics
        Rz = torch.tensor([[np.cos(angz), -np.sin(angz), 0],
                            [np.sin(angz), np.cos(angz), 0],
                            [0, 0, 1]], dtype=torch.float) # Construct rotation transform
        Rx = torch.tensor([[np.cos(angy), 0, np.sin(angy)],
                            [0, 1, 0.],
                            [-np.sin(angy), 0, np.cos(angy)]
                                    ], dtype=torch.float)
        Ry = torch.tensor([[1, 0, 0],
                            [0, np.cos(angx), -np.sin(angx)],
                            [0, np.sin(angx), np.cos(angx)]
                                    ], dtype=torch.float)
        
        # Get world rotation
        R = torch.mm(Ry, Rx)
        R = torch.mm(Rz, R)
        R = torch.cat([R.T, torch.tensor([[0., 0., 0.]], dtype=torch.float)],dim=0).T


        R = R.repeat(c2w.size(0), 1, 1).transpose(1,2) # One matrix for each view


        rotated_c2w = torch.bmm(R, c2w) # T = R_z * c2w

        cones_rotated = display_views_as_cones(rotated_c2w, col=2)


        # Write New extrinsics to file
        write_extrinsics(rotated_c2w, source, f, name=name)

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

            fig = go.Figure(data=[cones_original, cones_rotated, zaxis_line, yaxis_line, xaxis_line])
            # fig.show()



if __name__ == "__main__":

    rots = [90, 0, 0]
    main(*rots)

