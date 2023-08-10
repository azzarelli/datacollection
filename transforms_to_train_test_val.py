import os
from pathlib import Path
import json

source = Path("data/200im_360_view")

file_list = os.listdir(source)

assert file_list != [], 'File list empty - make sure correct folder is selected'

# Create folder
train_path = source / 'train'
test_path = source / 'test'
val_path = source / 'val'

# Remove folders if tey already exist (WARNING!!)
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

image_ids = []
frames = {}
# Go through the files in the folder to sort
for file in file_list:
    # Process the transforms file into 
    if 'transforms.json' == file:
        with open(source/file) as fp:
            contents = fp.read()
        meta = json.loads(contents)

        for frame in meta['frames']:
            fp = frame['file_path'].split('_')[-1] # get the image id
            frames[fp] = frame['file_path'].split('/')[-1] # get the image name
        print(meta.keys())
    # Process the images - where depth and normal flags aren't included in the original file name
    if '.png' in file and 'depth' not in file and 'normal' not in file:
        id = file.split('_')[1].split('.')[0] # Expecting fp names like r_0.png to turn into str('0')
        image_ids.append(int(id))

image_ids = sorted(image_ids)
dataset_size = len(image_ids) # get size of dataset to run dataset split



print(sorted(image_ids))
            
    

