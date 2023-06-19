import argparse
import os

TEST_DFP = './data/boat_colmap/'
TEST_VFP = './data/boat/boat.mp4'

def static_to_dynamic_dataset(d_fp, v_fp):
    """Convert static colmap data to dynamic data such as the data used in D-NeRF
    
    Args:
        d_fp, v_fp: str, data folder and video filepaths respectively 
    """
    assert os.path.exists(d_fp), 'Data file path does not exist'
    assert os.path.exists(v_fp), 'Video file path does not exist'
    assert '.mp4' == v_fp[-4:], 'Need mp4' # TODO: Test on other video formats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='PROG',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-d', '--data', default="/",
                    help='Static dataset folder (default: "")')

    parser.add_argument('-v', '--video', default="/",
                    help='Original video filepath (default: "")')
    
    args = vars(parser.parse_args())
    
    
    static_to_dynamic_dataset(TEST_DFP, TEST_VFP)
    # static_to_dynamic_dataset(args['data'], args['video'])