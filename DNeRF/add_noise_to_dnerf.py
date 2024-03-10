import os
from pathlib import Path
import json 
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
from tqdm import tqdm

datadir = Path('./data/dnerf/data/')
scene = 'trex'
DEBUG = False
mean = 0
sigma = .05


datadir = datadir / scene

# We only want to add noise to the training dataset
traindir = datadir /'train'
testdir = datadir /'test'
valdir = datadir /'val'
destination = datadir / 'train_noisy'
dest_test = datadir / 'test_noisy'
dest_val = datadir / 'val_noisy'


# Simple checks
if os.path.exists(destination) or os.path.exists(dest_test) or os.path.exists(dest_val):
    raise ValueError(f'Destination folder already exists - delete/rename before rerunning')

if not os.path.exists(datadir/'train') or not os.path.exists(datadir/'test') or not os.path.exists(datadir/'val'):
    raise ValueError('Input Folder does not exists')

if not os.path.exists(traindir) or  not os.path.exists(testdir) or  not os.path.exists(valdir):
    raise ValueError('Missing train dir with images')


def noise(img, mean, sigma):
    img = np.asarray(img).astype(np.float64) / 255. #.astype(np.float64)
    gaussian = np.random.normal(mean, sigma, (img.shape[0],img.shape[1], 4)) 
    # print(gaussian)
    dst= (img + gaussian)*255.
    # print(dst)
    dst = np.clip(dst, 0, 255)

    dst = (dst).astype(np.uint8)
    return Image.fromarray(dst)

# Downsample Ground Truths
gt_dirs = [testdir, valdir]
gt_dest = [dest_test, dest_val]

for dir, dest in zip(gt_dirs, gt_dest):
    if not DEBUG:
        os.mkdir(dest)

    images = os.listdir(dir)
    with tqdm(total=len(images), unit='image', desc=f'Downsampling') as pbar:
        for imfp in images:
            im = Image.open(dir/imfp)
            d = dest/imfp
            width, height = im.size
            
            out_w, out_h = int(width/2), int(height/2)
            im = im.resize((out_w, out_h), Image.LANCZOS)

            if DEBUG:
                im.show()
                exit()

            im.save(d)
            pbar.update(1)


if not DEBUG:
    os.mkdir(destination)
images = os.listdir(traindir)

img_set = {}
with tqdm(total=len(images), unit='image', desc='Adding Noise') as pbar:
    for imfp in images:
        im = Image.open(traindir/imfp)
        dest = destination / imfp
        width, height = im.size
        
        out_w, out_h = int(width/2), int(height/2)
        im = im.resize((out_w, out_h), Image.LANCZOS)

        noisy_im= noise(im, mean, sigma)

        if DEBUG:
            noisy_im.show()
            exit()

        noisy_im.save(dest)
        pbar.update(1)


