import os
import json

fp_ext = ['train', 'test', 'val']
fp_branch = 'data/boat_custom/transforms_'
fp_end = '.json'

for ext in fp_ext:
    fp = fp_branch+ext+fp_end
    
    with open(fp) as file:
        d = json.load(file)
    
    for frame in d['frames']:
        frame['file_path'] = frame['file_path'][:-4]
    
    with open(fp, 'w') as file:
        json.dump(d, file)