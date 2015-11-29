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
import scandir

from mosaic.utils import memoized

##########################################################################
## Module Constants
##########################################################################

DIRNODE   = "inode/directory"
FILENODE  = "inode/file"
LINKNODE  = "inode/symlink"
EMPTYNODE = "inode/x-empty"

##########################################################################
## Walking
##########################################################################

def walk(path, include_hidden=False):
    """
    Walk a directory, excluding hidden directories and depth.
    """

    for name, dirs, files in scandir.walk(path._path):
        name  = Path(name)
        files = [name.join(f) for f in files]
        dirs  = [name.join(d) for d in dirs]

        if not include_hidden:
            files   = filter(lambda p: p.is_hidden, files)
            dirs[:] = filter(lambda p: p.is_hidden, dirs)

        yield name, dirs, files, path.relative_depth(name)


def scan(path, include_hidden=False):
    """
    Scan a directory, excluding hidden directories. Yields paths.
    """

    for subpath in path.list():
        if not include_hidden and subpath.is_hidden():
            continue

        if subpath.is_dir():
            for path in subpath.list():
                yield path
        else:
            yield subpath


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


##########################################################################
## Path object
##########################################################################

class Path(object):
    """
    Wraps a path string and performs common operations on it.
    Note that the string is automatically expanded from user and env vars.
    """

    @classmethod
    def from_entry(klass, entry):
        """
        Creates a path from a scandir DirEntry.
        """
        # Initialize the path with various attributes.
        path = klass(entry.path, inode=entry.inode())
        path._nodestat = entry.stat(follow_symlinks=False)

        # Set the nodetype on the path
        if entry.is_dir(follow_symlinks=False):
            path._nodetype = DIRNODE
        elif entry.is_file(follow_symlinks=False):
            path._nodetype = FILENODE
        elif entry.is_symlink():
            path._nodetype = LINKNODE
        else:
            path._nodetype = None

        return path

    def __init__(self, path, **kwargs):
        # Copy from another path if passed in
        if isinstance(path, Path):
            path = path._path

        # Perform default Path manipulations
        path = os.path.expandvars(os.path.expanduser(path))

        # Set various path information
        self._path     = path
        self._nodetype = None
        self._nodestat = None

    def __str__(self):
        return self._path

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, str(self))

    def __add__(self, other):
        return self.join(other)

    def __eq__(self, other):
        if isinstance(other, Path):
            return self._path == other._path
        return self._path == other

    @memoized
    def inode(self):
        if self._nodestat is None:
            self._nodestat = os.stat(self._path)
        return self._nodestat.st_ino

    @memoized
    def mimetype(self):
        return magic.from_file(self._path, mime=True)

    @memoized
    def filesize(self):
        if self._nodestat is None:
            self._nodestat = os.stat(self._path)
        return self._nodestat.st_size

    def exists(self):
        return os.path.exists(self._path)

    def is_symlink(self):
        if self._nodetype is None:
            self._nodetype = LINKNODE if os.path.islink(self._path) else None
        return self._nodetype == LINKNODE

    def is_dir(self):
        if self._nodetype is None:
            self._nodetype = DIRNODE if os.path.isdir(self._path) else None
        return self._nodetype == DIRNODE

    def is_file(self):
        if self._nodetype is None:
            self._nodetype = FILENODE if os.path.isfile(self._path) else None
        return self._nodetype == FILENODE

    def is_empty(self):
        if self._nodetype is None:
            if self.is_file():
                if self.filesize == 0:
                    self._nodetype = EMPTYNODE
        return self._nodetype == EMPTYNODE

    def is_hidden(self):
        """
        Returns if the path is hidden or not.
        """
        basename = os.path.basename(self._path)
        return basename[0] in {'.', '~'}

    def join(self, *subpath):
        """
        Joins another path and returns a new path.
        """
        # Stringify paths in order to pass to join.
        subpath = map(str, subpath)
        return Path(os.path.join(self._path, *subpath))

    def list(self):
        """
        Returns a generator of paths inside of a directory.
        This uses the scandir function for speed and reliability.
        """
        for entry in scandir.scandir(self._path):
            yield Path.from_entry(entry)

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
