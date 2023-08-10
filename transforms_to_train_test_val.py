import os
from pathlib import Path
import json
import random
import shutil

source = Path("./data/200im_360_view")

file_list = os.listdir(source)
train_split = 0.9 # Set the dataset split ratios
test_split = 0.08
val_split = 0.02
random.seed(42)

linked_fp_flag = ['_depth', '_normal'] # if images have linked depth and normal renders they'll usually be denotes e.g. as 'r_0_depth.png' or similar
                                    # We want to move these files as well...


assert (train_split + test_split + val_split == 1.), 'Make sure data split adds up to 1.'
assert file_list != [], 'File list empty - make sure correct folder is selected.'
assert os.path.exists(source/'transforms.json'), 'No transforms.json file found in directory'

# Create image folders
train_path = source / 'train'
test_path = source / 'test'
val_path = source / 'val'

# Remove folders if they already exist (WARNING!!)
if os.path.exists(train_path):
    os.rmdir(train_path)
if os.path.exists(test_path):
    os.rmdir(test_path)
if os.path.exists(val_path):
    os.rmdir(val_path)
# Make folder in root
os.mkdir(test_path)
os.mkdir(train_path)
os.mkdir(val_path)

# Process data from 'transforms.json'
with open(source/'transforms.json') as fp:
    contents = fp.read()
meta = json.loads(contents) # load data as dict
frames = meta['frames'] # get frame data
dataset_size = len(frames) # get size of dataset
random.shuffle(frames) # shuffle data


# Split shuffled data
train_idx = int(train_split * dataset_size)
test_idx = train_idx + int(test_split * dataset_size)

# Ensure we have atleast one image the val folder 
assert len(frames[test_idx:]) > 0, 'Ensure `val_split` is large enough to have atleast 1 image in dataset'

# Define our seperate dataset
train_frames = frames[:train_idx]
test_frames = frames[train_idx:test_idx]
val_frames = frames[test_idx:]

def move_files(targ_path, frame, file_list):
    image_id = frame['file_path'].split('/')[-1]
    fp_ = targ_path / (image_id+'.png')  # append end of file path to new image path

    shutil.move(source/(image_id+'.png'), source/fp_) # move source image to destination

    # Also append linked images if they exist
    for flag in linked_fp_flag:
        linked_fp = image_id + flag # substring of image name (e.g. 'r_0_depth' in 'r_0_depth_0250.png')
        linked_fp_ = [file_path for file_path in file_list if linked_fp in file_path][0] # get the whole string
       
        shutil.move(source/linked_fp_, source/targ_path/linked_fp_)
        
    return str(fp_)

# Process frames for training, testing and validation
for frame in train_frames:
    frame['file_path'] = move_files(Path('train'), frame, file_list)


for frame in test_frames:
    frame['file_path'] = move_files(Path('test'), frame, file_list)
    
for frame in val_frames:
    frame['file_path'] = move_files(Path('val'), frame, file_list)

# Set the transforms file format you desire
train_tranform = {'camera_angle_x': meta['camera_angle_x'],
                    'frames': train_frames
                 }
    
test_tranform = {'camera_angle_x': meta['camera_angle_x'],
                    'frames': test_frames
                 }

val_tranform = {'camera_angle_x': meta['camera_angle_x'],
                    'frames': val_frames
                 }

# Remove transforms files if they exist
if os.path.exists(source / 'transforms_train.json'):
    os.remove(source / 'transforms_train.json')
if os.path.exists(source / 'transforms_test.json'):
    os.remove(source / 'transforms_test.json')
if os.path.exists(source / 'transforms_val.json'):
    os.remove(source / 'transforms_val.json')

# Write the seperate transforms files
with open(source / 'train_transforms.json', 'w') as out_file:
    json.dump(train_tranform, out_file, indent=4)
    
with open(source / 'test_transforms.json', 'w') as out_file:
    json.dump(test_tranform, out_file, indent=4)

with open(source / 'val_transforms.json', 'w') as out_file:
    json.dump(val_tranform, out_file, indent=4)