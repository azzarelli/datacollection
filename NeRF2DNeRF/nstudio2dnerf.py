nerfstudio_fp ='/home/xi22005/Desktop/datacollection/outdoor'
output_fp = 'outputs'
transforms_fp = 'transforms.json'

import os
from pathlib import Path
import json
import shutil
import copy
from sklearn.model_selection import train_test_split

# Set dirs as paths
nerfstudio_fp = Path(nerfstudio_fp)
output_fp = nerfstudio_fp / output_fp
transforms_fp = nerfstudio_fp / transforms_fp

# TODO: Folder utils

assert nerfstudio_fp.exists(), f'Folder does not exist: {nerfstudio_fp}'
assert transforms_fp.exists(), f'Folder does not exist: {transforms_fp}'

if not os.path.exists(output_fp):
    print('Making new folder - ', output_fp)
    os.mkdir(output_fp)

print('Making: train/test/val folders')
if not os.path.exists(output_fp / 'train'):
    os.mkdir(output_fp / 'train')
if not os.path.exists(output_fp / 'test'):
    os.mkdir(output_fp / 'test')
if not os.path.exists(output_fp / 'val'):
    os.mkdir(output_fp / 'val')
# We won't remove files inside of these folders as they wont be referenced in the transforms file so pointless (and I cba)

print(f'Loading transfroms file...')
with open(transforms_fp, 'r') as f:
    obj = json.load(f)

# Load the intrinsics
intrinsics = {}
for key in obj.keys():
    if key != 'frames':
        intrinsics[key] = obj[key]

frames = obj['frames']

# Assign a index to each frame depending on the  file name
#    Note: This relies on the assumption that frame 200 is captured earlier than frame 201
#          but we do not need a complete list
print('Determining time for each frame...')
for frame in frames:
    # Turn 'images/frame_00208.png' ->208
    f_name = int(frame['file_path'].split('/')[-1].split('.')[0].split('_')[-1])
    frame['id'] = f_name

# Sort frames
sorted_frames = sorted(frames, key=lambda x: x['id'])

max_T = len(sorted_frames)-1 # we use '-1' because we want to be 0. <= x <= 1. not 0<= x < 1.
# Add a time value for each frame
for t_idx, frame in enumerate(sorted_frames):
    time = float(t_idx/max_T)
    frame['time'] = time


print('Saving new frames in output directory...')
train_frames = []
for frame in sorted_frames:
    train_frames.append(copy.deepcopy(frame))

    train_frames[-1]['file_path'] = './train/r_'+str(frame['id']).zfill(5)

    # Copy from images folder to new training folder
    shutil.copy(nerfstudio_fp / frame['file_path'],
                output_fp / ('train/r_'+str(frame['id']).zfill(5)+'.'+frame['file_path'].split('.')[-1]))


train_data, test_data = train_test_split(train_frames, test_size=0.1, random_state=42)



print('Saving new transforms...')
final_transforms = intrinsics

final_transforms['frames'] = train_data
with open(output_fp/'transforms_train.json', 'w') as f:
    json.dump(final_transforms, f, indent=4)

final_transforms['frames'] = test_data
with open(output_fp/'transforms_test.json', 'w') as f:
    json.dump(final_transforms, f, indent=4)

print('Done')