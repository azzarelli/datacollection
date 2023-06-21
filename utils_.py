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
    