# mosaic.console.main
# The main mosaic command line utility program
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sat Nov 28 12:45:23 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: main.py [] benjamin@bengfort.com $

"""
The main mosaic command program.
"""

##########################################################################
## Imports
##########################################################################

import mosaic

from mosaic.console.commands import *
from mosaic.console.prog import ConsoleProgram

##########################################################################
## Command Line Variables
##########################################################################

DESCRIPTION = "Inspects the mimetype distribution of a directory."
EPILOG      = "Created for scientific purposes and not diagnostic ones."
COMMANDS    = [
    UsageCommand,
]

##########################################################################
## The Mosaic Command line Program
##########################################################################

class MosaicUtility(ConsoleProgram):

    description = DESCRIPTION
    epilog      = EPILOG
    version     = mosaic.__version__

    @classmethod
    def load(klass, commands=COMMANDS):
        utility = klass()
        for command in commands:
            utility.register(command)
        return utility
