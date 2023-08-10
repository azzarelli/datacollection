import os
from pathlib import Path
import json
import random
source = Path("data/200im_360_view")

file_list = os.listdir(source)
train_split = 0.9 # Set the dataset split ratios
test_split = 0.08
val_split = 0.02

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
with open(source/file) as fp:
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

    train_frames = frames[:train_idx]
    test_frames = frames[train_idx:test_idx]
    val_frames = frames[test_idx:]

for frame in train_frames:
    fp_ = train_path / frame['file_path'].split('/')[-1] # append end of file path to new image path
    


image_ids = []
frames = {}
# Go through the files in the folder to sort
for file in file_list:
    # Process the transforms file into 
    if 'transforms.json' == file:
        
        
        
        for frame in meta['frames']:
            frame_fp = frame['file_path'].split('/')[-1] # get the image name
        print(meta.keys())
    # Process the images - where depth and normal flags aren't included in the original file name
    if '.png' in file and 'depth' not in file and 'normal' not in file:
        id = file.split('_')[1].split('.')[0] # Expecting fp names like r_0.png to turn into str('0')
        image_ids.append(int(id))

image_ids = sorted(image_ids)
dataset_size = len(image_ids) # get size of dataset to run dataset split



print(sorted(image_ids))
            
    

