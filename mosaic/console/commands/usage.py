# mosaic.console.commands.usage
# Performs file system usage analysis on a given directory.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sat Nov 28 12:51:49 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: list.py [] benjamin@bengfort.com $

"""
Performs file system usage analysis on a given directory.
"""

##########################################################################
# Imports
##########################################################################

import time

from mosaic.path import Path
from mosaic.usage import analyze
from mosaic.console.commands.base import Command

##########################################################################
## Helper functions
##########################################################################

def path(val):
    val = Path(val)
    if val.exists() and val.is_dir():
        return str(val.join('mosaic-{}.json'.format(int(time.time()))))
    return str(val)

##########################################################################
# Command
##########################################################################

class UsageCommand(Command):

    name = "usage"
    help = "enumerate the simulations available for execution"

    args = {
        ('-I', '--include-hidden'): {
            'action': 'store_true',
            'help': 'include hidden files and directories',
        },
        ('-o', '--output'): {
             'metavar': 'PTH',
             'type': path,
             'default': '.',
             'help': 'path or directory to write output to',
        },
        'path': {
            'nargs': 1,
            'help': 'path of directory to inspect',
        }
    }

    def handle(self, args):
        """
        Handle command line arguments
        """
        usage = analyze(args.path[0], args.include_hidden)
        with open(args.output, 'w') as f:
            usage.dump(f, indent=2)

        return str(usage)
