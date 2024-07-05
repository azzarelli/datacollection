import os
from argparse import ArgumentParser
from pathlib import Path
import numpy as np


if __name__ == "__main__":
    parser = ArgumentParser(description="Training script parameters")
    parser.add_argument('--directory', type=str, default = "")

    args = parser.parse_args()

    # Get path of camera params
    full_pth = Path(args.directory) / 'poses_bounds.npy'

    # Check exists and display cam positions
    if os.path.exists(full_pth):
        print('Dynerf data found!')

        pose_arr = np.load(full_pth)

        poses = pose_arr[:, :-2].reshape([-1, 3, 5])  # (N_cams, 3, 5)
        near_fars = pose_arr[:, -2:]
        H, W, focal = poses[0, :, -1]
        focal = [focal, focal]
        poses = np.concatenate([poses[..., 1:2], -poses[..., :1], poses[..., 2:4]], -1)


        # Load relevant display libraries
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.quiver(0, 0, 0, 0, 0, 0, color='k', arrow_length_ratio=0.1) # Origin

        # For each ppose extract the rotation and position
        for pose in poses:
            R = pose[:3,:3]
            R = -R
            R[:,0] = -R[:,0]
            T = -pose[:3,3].dot(R)
            
        print(poses.shape)
