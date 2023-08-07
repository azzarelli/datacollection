import os

def pathchecks(pathlist):
    """Validate paths given for existing

    Args:
        pathlist, list, 1-D list containing paths
    """

    for path in pathlist:
        assert path.exists(), f'Error: {path} does not exist.'

def folderchecks(pathlist):
    """Validate paths given as folder

    Args:
        pathlist, list, 1-D list containing paths
    """

    for path in pathlist:
        assert path.is_dir(), f'Error: {path} does not exist as a folder.'

import json

def load_from_json(fp_data):
    with open(fp_data) as fp:
        contents = fp.read()
    meta = json.loads(contents)
    return meta