import os
from pathlib import Path
import json 
import matplotlib.pyplot as plt
import numpy as np

datadir = Path('./data/dnerf/data/')
scene = 'trex'
boomerangs = 10

testdir = (datadir / scene) /'transforms_test.json'
traindir = (datadir / scene) /'transforms_train.json'
valdir = (datadir / scene) /'transforms_val.json'

destination = datadir / (scene+'_boomerang')

# Simple checks
if os.path.exists(destination):
    raise ValueError(f'Destination folder already exists - delete/rename before rerunning')

if not os.path.exists(datadir / scene):
    raise ValueError('Input Folder does not exists')

if not os.path.exists(testdir) or not os.path.exists(traindir) or not os.path.exists(valdir):
    raise ValueError('Missing transforms_[].json files')

# Create timeline
transforms = {}
t = open(testdir)
transforms['test'] = json.load(t)
t.close()

t = open(traindir)
transforms['train'] = json.load(t)
t.close()
t = open(valdir)
transforms['val'] = json.load(t)
t.close()

times = []
what = []
col = []
for t_key in transforms.keys():
    for frame in transforms[t_key]['frames']:
        if t_key == 'test': 
            what.append(0)
            col.append('red')
        elif t_key == 'train': 
            what.append(1)
            col.append('blue')
        else: 
            col.append('green')
            what.append(2)
        times.append(frame['time'])

"""
At each iteration we want to reverse the order of images data and 
"""
fwd_times = np.array(times)
indexs = np.linspace(0, len(times)-1, len(times))

# Sort all data relative to time and keep note of the original index
# 0 to 1 order
sorted_indices = np.argsort(fwd_times)

fwd_times = fwd_times[sorted_indices]
fwd_indexs = indexs[sorted_indices]

# Flip the frame sequence and correct times (0 to 1)
bck_times = np.abs((np.flip(fwd_times)-1.))
bck_indexs = np.flip(indexs)

it_start_time = 0.
timestack = None
indstack = None
for i in range(boomerangs):
    # Even = forward facing in time
    if (i % 2) == 0: 
        t = fwd_times
        ind = fwd_indexs 
    else: # Odd = backward facing in time (reflection)
        t = bck_times
        ind = bck_indexs
    t = t + it_start_time

    # stack reverse data
    if i == 0: 
        timestack = t
        indstack = ind
    else: 
        timestack = np.concatenate([timestack, t])
        indstack = np.concatenate([indstack, ind])
    it_start_time += 1.


ind = 0
total = 3.

train = []
test = []
val = []

for t_key in transforms.keys():
    for frame in transforms[t_key]['frames']:
        
        selected_ind = np.where(indstack == ind)[0]
        selected_times = timestack[selected_ind]

        for t in selected_times:
            frame_ = frame.copy()
            frame_['time'] = t/boomerangs
            
            if t_key == 'train': 
                # print(frame_)
                train.append(frame_)
            elif t_key == 'test': test.append(frame_)
            elif t_key == 'val': val.append(frame_)
            
        ind += 1

train = {'frames':train}
test = {'frames':test}
val = {'frames':val}

train['camera_angle_x'] = transforms['train']['camera_angle_x']
test['camera_angle_x'] = transforms['test']['camera_angle_x']
val['camera_angle_x'] = transforms['val']['camera_angle_x']

os.mkdir(destination)
with open(destination/'transforms_train.json', "w") as outfile:
    json.dump(train, outfile, indent=4)
with open(destination/'transforms_test.json', "w") as outfile:
    json.dump(test, outfile, indent=4)
with open(destination/'transforms_val.json', "w") as outfile:
    json.dump(val, outfile, indent=4)

# # print(train)


print(len(val['frames']))
