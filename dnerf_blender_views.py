# A simple script that uses blender to render views of a single object by rotation the camera around it.
# Also produces depth map at the same time.

import argparse, sys, os
import json
import bpy
import mathutils
import numpy as np

# Get scene pointer
scene = bpy.context.scene
            
MAX_FRAME = scene.frame_end # Number of total frames in our scene
RESOLUTION = 800
RESULTS_PATH = 'results_two_camera_test'
COLOR_DEPTH = 8
FORMAT = 'PNG'
CAMERAS = [scene.objects['Camera'], scene.objects['Camera.001']]


fp = bpy.path.abspath(f"//{RESULTS_PATH}")


def listify_matrix(matrix):
    matrix_list = []
    for row in matrix:
        matrix_list.append(list(row))
    return matrix_list

if not os.path.exists(fp):
    os.makedirs(fp)
    os.makedirs(fp+'images')    
if not os.path.exists(fp+'images'):
    os.makedirs(fp+'images')

# Data to store in JSON file
out_data = {
    'camera_angle_x': bpy.data.objects['Camera'].data.angle_x,
}

# Render Optimizations
bpy.context.scene.render.use_persistent_data = True


# Set up rendering of depth map.
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

# Add passes for additionally dumping albedo and normals.
#bpy.context.scene.view_layers["RenderLayer"].use_pass_normal = True
bpy.context.scene.render.image_settings.file_format = str(FORMAT)
bpy.context.scene.render.image_settings.color_depth = str(COLOR_DEPTH)


# Background
bpy.context.scene.render.dither_intensity = 0.0
bpy.context.scene.render.film_transparent = True

# Set scene constraints
scene.render.resolution_x = RESOLUTION
scene.render.resolution_y = RESOLUTION
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'  # set output format to .png


# Initialise output data for each view
out_data['frames'] = []
img_dir = './images/'

# Loop through all the cameras
for j, cam in enumerate(CAMERAS):
    # Set the Active Camera
    scene.camera = cam
    
    # Loop through the frames to render and save
    for i in range(0, MAX_FRAME):
        # Determine the current frame and Set it
        frame = int( (i / (MAX_FRAME-1)) * MAX_FRAME)
        bpy.context.scene.frame_set(frame)
        
        print('Time:', frame, 'Cam: ', j)
        
        # Set the frame name (for render and to save reference in transforms.json)
        view_name = 'r_{0:03d}'.format(frame) + f'_{j}'
        
        # Set the rendering file_path
        scene.render.filepath = fp + '/images/' + view_name
        
        # Render
        bpy.ops.render.render(write_still=True) 
        
        # Save individual frame data
        frame_data = {
            'file_path': img_dir + view_name,
            'rotation': 0.001,
            'time': float(i / (NUM_FRAMES-1)),
            'transform_matrix': listify_matrix(cam.matrix_world),
        }
        
        # Append to output file
        out_data['frames'].append(frame_data)


with open(fp + '/' + 'transforms.json', 'w') as out_file:
    json.dump(out_data, out_file, indent=4)
