import argparse
import os

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
    else:
        print(f'Path: {new_dir_fp} already exists! Manually delete this to overide')
        exit()
    
    

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