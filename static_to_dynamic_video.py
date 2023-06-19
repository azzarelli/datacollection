import argparse
import os

def static_to_dynamic_dataset(d_fp, v_fp):
    """Convert static colmap data to dynamic data such as the data used in D-NeRF
    
    Args:
        d_fp, v_fp: str, data folder and video filepaths respectively 
    """


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='PROG',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-d', '--data', default="/",
                    help='Static dataset folder (default: "")')

    parser.add_argument('-v', '--video', default="/",
                    help='Original video filepath (default: "")')
    
    args = vars(parser.parse_args())

    print(args['data'], args['video'])