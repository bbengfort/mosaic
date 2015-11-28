# mosaic.utils
# Utilities for the mosaic package.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sat Nov 28 07:05:28 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: utils.py [] benjamin@bengfort.com $

"""
Utilities for the mosaic module.
"""

##########################################################################
## Imports
##########################################################################

from mosaic.path import Path

##########################################################################
## File System Utilities
##########################################################################

def get_tree_size(path):
    """
    Return total size of all files in directory tree at path.
    Note: this is not part of the Path object for brevity.
    """
    if not isinstance(path, Path):
        path = Path(path)

    def get_size(path):
        try:
            if path.is_symlink(): return 0
            if path.is_dir(): return get_tree_size(path)
            return path.filesize
        except OSError:
            return 0

    return sum(get_size(subpath) for subpath in path.list())
