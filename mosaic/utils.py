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

import json
import time

from functools import wraps

##########################################################################
## Memoization
##########################################################################

def memoized(fget):
    """
    Return a property attribute for new-style classes that only calls its
    getter on the first access. The result is cached for reuse.
    """
    attr_name = "_{}".format(fget.__name__)

    @wraps(fget)
    def fget_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fget(self))
        return getattr(self, attr_name)

    return property(fget_memoized)


##########################################################################
## JSON encoding
##########################################################################

class MosaicEncoder(json.JSONEncoder):

    JSON_DATETIME    = "%Y-%m-%dT%H:%M:%S.%fZ"

    def encode_datetime(self, obj):
        """
        Converts a datetime object into epoch time.
        """
        return obj.strftime(self.JSON_DATETIME)

    def encode_Path(self, obj):
        return str(obj)

    def default(self, obj):
        """
        Perform encoding of complex objects.
        """
        try:
            return super(MosaicEncoder, self).default(obj)
        except TypeError:
            # If object has a serialize method, return that.
            if hasattr(obj, 'serialize'):
                return obj.serialize()

            # Look for an encoding method on the Encoder
            method = "encode_%s" % obj.__class__.__name__
            if hasattr(self, method):
                method = getattr(self, method)
                return method(obj)

            # Not sure what is going on if the above two methods didn't work
            raise TypeError(
                "Could not encode type '{0}' using {1}\n"
                "Either add a serialze method to the object, or add an "
                "encode_{0} method to {1}".format(
                    obj.__class__.__name__, self.__class__.__name__
                )
            )

##########################################################################
## Timer functions
##########################################################################

class Timer(object):
    """
    A context object timer. Usage:
        >>> with Timer() as timer:
        ...     do_something()
        >>> print timer.interval
    """

    def __init__(self, wall_clock=True):
        """
        If wall_clock is True then use time.time() to get the number of
        actually elapsed seconds. If wall_clock is False, use time.clock to
        get the process time instead.
        """
        self.wall_clock = wall_clock
        self.time = time.time if wall_clock else time.clock

    def __enter__(self):
        self.start    = self.time()
        return self

    def __exit__(self, type, value, tb):
        self.finish   = self.time()
        self.interval = self.finish - self.start

    def __str__(self):
        return humanizedelta(seconds=self.interval)

    def __unicode__(self):
        return decode(str(self))


def timeit(func, wall_clock=True):
    """
    Returns the number of seconds that a function took along with the result
    """
    @wraps(func)
    def timer_wrapper(*args, **kwargs):
        """
        Inner function that uses the Timer context object
        """
        with Timer(wall_clock) as timer:
            result = func(*args, **kwargs)

        return result, timer
    return timer_wrapper
