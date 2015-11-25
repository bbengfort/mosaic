# mosaic.analyze
# Performs analysis of a file system usage.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Nov 25 17:30:48 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: analyze.py [] benjamin@bengfort.com $

"""
Performs analysis of a file system usage.
"""

##########################################################################
## Imports
##########################################################################

import time
import mosaic

from collections import Counter
from mosaic.path import Path, walk

##########################################################################
## Sequential analysis
##########################################################################

def analyze(root, include_hidden=False):
    """
    Sequential mimetype frequency and space consumption analysis
    """

    root  = Path(root)  # pathify the root path.
    nodes = Counter()   # inodes counts (e.g. file vs. directory)
    mimes = Counter()   # mimetype frequency
    store = Counter()   # mimetype storage in bytes
    start = time.time() # time how long the walk takes

    if not root.is_dir():
        raise TypeError("The root path must be a directory.")

    for dname, dirs, files, depth in walk(root, include_hidden):

        nodes['dirs']  += len(dirs)
        nodes['files'] += len(files)

        for fpath in files:
            try:
                mime = fpath.mimetype

                mimes[mime] += 1
                store[mime] += fpath.filesize
            except Exception as e:
                print str(e)
                continue

    return {
        'nodes':  nodes,
        'mimes':  mimes,
        'store':  store,
        'root':   str(root),
        'timer': {
            'begun':  start,
            'finish': time.time(),
            'elapsed': "{:0.3f} seconds".format(time.time() - start),
        },
        'include_hidden': include_hidden,
        'version': mosaic.get_version(),
    }
