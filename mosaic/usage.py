# mosaic.usage
# Performs analysis of a file system usage.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Nov 25 17:30:48 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: usage.py [] benjamin@bengfort.com $

"""
Performs analysis of a file system usage.
"""

##########################################################################
## Imports
##########################################################################

import json
import time
import mosaic

from datetime import datetime
from collections import Counter
from mosaic.path import Path, scan
from mosaic.utils import MosaicEncoder
from mosaic.utils import humanize_bytes

##########################################################################
## Module Constants
##########################################################################

# File Usage States
AWAITING = 0
UNDERWAY = 1
FINISHED = 2

# Node types
FILE = "files"
DIRS = "dirs"
LINK = "links"
UNKN = "unknown"


##########################################################################
## Sequential analysis
##########################################################################

def analyze(root, include_hidden=False):
    """
    Sequential mimetype frequency and space consumption analysis
    """

    root  = Path(root)  # pathify the root path.
    usage = FileUsage(root, include_hidden=include_hidden)

    if not root.is_dir():
        raise TypeError("The root path must be a directory.")

    usage.start()
    for path in scan(root, include_hidden):

        try:
            usage.update(path)
        except OSError:
            print str(e)
            continue

    usage.finish()
    return usage


##########################################################################
## File Usage Data Structure
##########################################################################

class FileUsage(object):
    """
    Basically a wrapper for a series of counter objects, this class
    provides an on update method of tracking the statistics that we're
    looking for, as well as combining them in a meaningful way.
    """

    @classmethod
    def load(klass, fobj):
        """
        Loads a FileUsage data structure from a file-like object.
        """
        data  = json.load(fobj)
        usage = klass(data['root'], **data['options'])

        # Update the counters
        for key in ('nodes', 'mimes', 'store'):
            hist = getattr(usage, key)
            hist.update(data[key])

        # Update the analysis metrics
        for key in ('started', 'finished', 'elapsed'):
            setattr(usage, key, data['timer'][key])

        # Update the analysis status
        if usage.finished is not None:
            usage.status = FINISHED
        elif usage.started is not None:
            usage.status = UNDERWAY
        else:
            usage.status = AWAITING

        return usage

    def __init__(self, root, **kwargs):
        self.root  = Path(root)
        self.nodes = Counter()
        self.mimes = Counter()
        self.store = Counter()

        # Analysis metrics
        self.started  = None
        self.finished = None
        self.elapsed  = None
        self.status   = AWAITING
        self.options  = kwargs

    def __iadd__(self, other):
        """
        In place addition of the counts of another usage object:

            >>> usage = FileUsage()
            >>> usage += other

        Not regular addition does not make sense because of the state tracking.
        """
        self.nodes += other.nodes
        self.mimes += other.mimes
        self.store += other.store

    def __str__(self):
        """
        Reports the usage and status of the analysis.
        """
        if self.status == FINISHED:
            return (
                "Discovered {} files, {} symlinks, and {} directories in {:0.3f} seconds"
                .format(self.nodes[FILE], self.nodes[LINK], self.nodes[DIRS], self.elapsed)
            )

        return  "Performing analysis of {}".format(self.root)

    @property
    def size(self):
        """
        Computes the total size (in bytes) of the usage.
        """
        return sum(val for val in self.store.values())

    @property
    def items(self):
        """
        Computes the total number of nodes in the usage.
        """
        return sum(val for val in self.nodes.values())

    @property
    def types(self):
        """
        Computes the number of different mimetypes in the usage.
        """
        return sum(1 for key in self.mimes)

    def start(self):
        """
        Helper function to start an analysis that this data structure is tracking.
        """
        self.started = time.time()
        self.status  = UNDERWAY

    def finish(self):
        """
        Helper function to complete an analysis that this data structure is tracking.
        """
        self.status   = FINISHED
        self.finished = time.time()
        self.elapsed  = self.finished - self.started

    def update(self, path):
        """
        Updates the counters and usage statistics for a given path.
        """
        # Update the node types
        if path.is_dir():
            self.nodes[DIRS] += 1

        elif path.is_file():
            self.nodes[FILE] += 1

            # Update the mimetype and storage
            self.mimes[path.mimetype] += 1
            self.store[path.mimetype] += path.filesize

        elif path.is_symlink():
            self.nodes[LINK] += 1

        else:
            self.nodes[UNKN] += 1

    def dump(self, fobj, **kwargs):
        """
        Dump the file usage as JSON to the file-like object.
        """
        json.dump(self.serialize(), fobj, cls=MosaicEncoder, **kwargs)

    def serialize(self):
        """
        Return a Python dictionary that represents the file usage.
        """
        return {
            'nodes':  self.nodes,
            'mimes':  self.mimes,
            'store':  self.store,
            'root':   self.root,
            'size':   humanize_bytes(self.size),
            'items':  self.items,
            'types':  self.types, 
            'timer': {
                'started':  datetime.utcfromtimestamp(self.started),
                'finished': datetime.utcfromtimestamp(self.finished),
                'elapsed':  self.elapsed,
            },
            'options': self.options,
            'version': mosaic.get_version(),
        }
