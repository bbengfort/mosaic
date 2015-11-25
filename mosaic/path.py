# mosaic.path
# Wrapper for common path based operations
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Nov 25 16:58:41 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: path.py [] benjamin@bengfort.com $

"""
Wrapper for common path based operations
"""

##########################################################################
## Imports
##########################################################################

import os
import magic

DIRNODE  = "inode/directory"
FILENODE = "inode/file"

##########################################################################
## Walking
##########################################################################

def walk(path, include_hidden=False):
    """
    Walk a directory, excluding hidden directories and depth.
    """

    for name, dirs, files in os.walk(path._path):
        name  = Path(name)
        files = [name.join(f) for f in files]
        dirs  = [name.join(d) for d in dirs]

        if not include_hidden:
            files   = filter(lambda p: p.is_hidden, files)
            dirs[:] = filter(lambda p: p.is_hidden, dirs)

        yield name, dirs, files, path.relative_depth(name)


##########################################################################
## Path object
##########################################################################

class Path(object):
    """
    Wraps a path string and performs common operations on it.
    Note that the string is automatically expanded from user and env vars.
    """

    def __init__(self, path):
        # Copy from another path if passed in
        if isinstance(path, Path):
            path = path._path

        # Set various path information
        self._path = os.path.expandvars(os.path.expanduser(path))
        self._mimetype = None
        self._nodetype = None
        self._filesize = None
        self._nodestat = None

    def __str__(self):
        return self._path

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, str(self))

    def __add__(self, other):
        return self.join(other)

    @property
    def mimetype(self):
        if self._mimetype is None:
            self._mimetype = magic.from_file(self._path, mime=True)
        return self._mimetype

    @property
    def filesize(self):
        if self._nodestat is None:
            self._nodestat = os.stat(self._path)
        return self._nodestat.st_size

    def exists(self):
        return os.path.exists(self._path)

    def is_dir(self):
        if self._nodetype is None:
            self._nodetype = DIRNODE if os.path.isdir(self._path) else None
        return self._nodetype == DIRNODE

    def is_file(self):
        if self._nodetype is None:
            self._nodetype = FILENODE if os.path.isfile(self._path) else None
        return self._nodetype == FILENODE

    def is_hidden(self):
        """
        Returns if the path is hidden or not.
        """
        basename = os.path.basename(self._path)
        return basename[0] in {'.', '~'}

    def join(self, subpath):
        """
        Joins another path and returns a new path.
        """
        if isinstance(subpath, Path):
            subpath = subpath._path
        return Path(os.path.join(self._path, subpath))

    def list(self):
        """
        Returns a generator of paths inside of a directory.
        """
        for name in os.listdir(self._path):
            yield self.join(name)

    def relative_depth(self, subpath):
        """
        Compares the relative depth of a subpath to this path.
        """
        if not isinstance(subpath, Path):
            subpath = Path(subpath)

        if not subpath._path.startswith(self._path):
            subpath = self.join(subpath)

        depth = self._path.count(os.sep)
        return subpath._path.count(os.sep) - depth
