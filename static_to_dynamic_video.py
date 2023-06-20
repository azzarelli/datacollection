import argparse
import os
import cv2
import json
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse

from tqdm import tqdm

TEST_DFP = './data/boat_colmap/'
TEST_VFP = './data/boat/boat.mp4'

def static_to_dynamic_dataset(d_fp, v_fp, img_fp):
    """Convert static colmap data to dynamic data such as the data used in D-NeRF
    
    Args:
        d_fp, v_fp: str, data folder and video filepaths respectively 
        img_fp: str, the image folder within the data fp
    """
    assert os.path.exists(d_fp), 'Data file path does not exist'
    assert os.path.exists(v_fp), 'Video file path does not exist'
    assert '.mp4' == v_fp[-4:], 'Need mp4' # TODO: Test on other video formats

    if d_fp[-1] != '/': d_fp += '/'
    img_fp = d_fp+img_fp+'/'
    tf_fp = d_fp+'transforms.json'
    assert os.path.exists(img_fp), 'Image folder path does not exist'
    assert os.path.exists(tf_fp), 'Could not find transforms.json'
    
    new_dir_fp = d_fp+'dynamic/'
    if not os.path.exists(new_dir_fp):
        os.makedirs(new_dir_fp)
    # else:
    #     print(f'Path: {new_dir_fp} already exists! Manually delete this to overide')
    #     exit()
    
    # Load transforms json
    with open(tf_fp) as fp:
        contents = fp.read()
    transforms = json.loads(contents)
    img_frames = transforms['frames']
    

    #  Load video
    video = cv2.VideoCapture(v_fp)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f'Total number of frames to process {total_frames}')

    sorted_data = []

    iterator = tqdm(range(0, total_frames))

    for i in iterator:

        # TODO: Maybe we jsut nead cv2.read as we loop through all frames anyways
        video.set(cv2.CAP_PROP_FRAME_COUNT, i)
        ret, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
        ssims = []
        ssim_max = 0.
        for idx, img_frame in enumerate(img_frames):
            # print(img_frame)
            img_frame_fp = d_fp+img_frame['file_path']
            image = cv2.imread(img_frame_fp, cv2.IMREAD_GRAYSCALE)
            
            ssim_res = ssim(image, frame)
            if ssim_res > ssim_max:
                ssim_max = ssim_res
                ssims = []
                ssims.append(idx)
            elif ssim_res == ssim_max:
                ssims.append(idx)
        
        # Lets ignore frames if its not close enough
        if ssim_max < 0.95:
            break

        idx_min = min(ssims)
        idx_data = img_frames[idx_min]
        del img_frames[idx_min]

        sorted_data.append({
            "idx": i,
            "data": idx_data
        })
        # comment out after test
        # break
        # if i == 4:
        #     break

    # For each value in sorted_data we should have a frame index (time point) and data
    #  We now need to split into train test and validation and insert additional metadata
    tt_split = 0.9 # ratio of dataset to assign to training, remainder will be assigned to testing and validation
    tv_split = 0.9 # ration of test data set to assign subsequent split to test and validation

    train_index = int(len(sorted_data) * tt_split) # 0 to train_index is training dataset
    test_index = train_index + int((len(sorted_data) - train_index) * tv_split) # train_index to test_index is the testing dataset, so test_index to len(data) is the val dataset 
    train_data = sorted_data[0:train_index]
    test_data = sorted_data[train_index:test_index]
    val_data = sorted_data[test_index:]
    
    
    train_file = {
        "camera_angle_x": 0.6911112070083618,
        "frames":[]
    }

    local_properties = {
        "rotation": 0.3141592653589793,

    }

    for data in train_data:
        time = float(data['idx'] / total_frames)
        fname = data['data']['file_path'].split('/')[-1]

        train_file["frames"].append({
            "file_path":f'./train/{fname}',
            "rotation": local_properties['rotation'],
            "time":time,
            "transform_matrix":data['data']['transform_matrix']
        })
    
    with open('transforms_train.json', 'w') as fp:
        json.dump(train_file, fp)       


    test_file = {
        "camera_angle_x": 0.6911112070083618,
        "frames":[]
    }
    for data in test_data:
        time = float(data['idx'] / total_frames)
        fname = data['data']['file_path'].split('/')[-1]

        test_file["frames"].append({
            "file_path":f'./train/{fname}',
            "rotation": local_properties['rotation'],
            "time":time,
            "transform_matrix":data['data']['transform_matrix']
        })
    
    with open('transforms_test.json', 'w') as fp:
        json.dump(test_file, fp)   
    

    val_file = {
        "camera_angle_x": 0.6911112070083618,
        "frames":[]
    }
    for data in val_data:
        time = float(data['idx'] / total_frames)
        fname = data['data']['file_path'].split('/')[-1]

        val_file["frames"].append({
            "file_path":f'./train/{fname}',
            "rotation": local_properties['rotation'],
            "time":time,
            "transform_matrix":data['data']['transform_matrix']
        })
    
    with open('transforms_val.json', 'w') as fp:
        json.dump(val_file, fp)  
    
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='PROG',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-d', '--data', default="/",
                    help='Static dataset folder (default: "")')

    parser.add_argument('-v', '--video', default="/",
                    help='Original video filepath (default: "")')
    
    parser.add_argument('-s', '--downscale', default="1",
                    help='Original datset has a downscale option. You can choose 1, 2, 4, 8 for folders images, images_2, images_4, images_8 (default: "")')
    
    args = vars(parser.parse_args())
    


    img_fp = 'images'
    if args['downscale'] != '1':
        img_fp += '_' + args['downscale']
    


    static_to_dynamic_dataset(TEST_DFP, TEST_VFP, img_fp)
    # static_to_dynamic_dataset(args['data'], args['video'])