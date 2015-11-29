#!/usr/bin/env python
# setup
# Setup script for installing mosaic
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Nov 25 06:50:44 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: setup.py [] benjamin@bengfort.com $

"""
Setup script for installing mosaic
"""

##########################################################################
## Imports
##########################################################################

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\"."
                      "Please install the setuptools package.")

##########################################################################
## Package Information
##########################################################################

# Read the __init__.py file for version info
version = None
versfile = os.path.join(os.path.dirname(__file__), "mosaic", "__init__.py")
with open(versfile, 'r') as versf:
    exec(versf.read(), namespace)
    version = namespace['get_version']()

## Discover the packages
packages = find_packages(where=".", exclude=("tests", "bin", "docs", "fixtures", "register", "notebooks"))

## Load the requirements
requires = []
with open('requirements.txt', 'r') as reqfile:
    for line in reqfile:
        requires.append(line.strip())

## Define the classifiers
classifiers = (
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
)

## Define the keywords
keywords = ('mosaic', 'usage', 'filesystem')

## Define the description
long_description = ""

## Define the configuration
config = {
    "name": "Mosaic",
    "version": version,
    "description": "User space file system usage analysis tool.",
    "long_description": long_description,
    "license": "MIT",
    "author": "Benjamin Bengfort",
    "author_email": "bengfort@cs.umd.edu",
    "url": "https://github.com/bbengfort/mosaic",
    "download_url": 'https://github.com/bbengfort/mosaic/tarball/v%s' % version,
    "packages": packages,
    "install_requires": requires,
    "classifiers": classifiers,
    "keywords": keywords,
    "zip_safe": True,
    "scripts": ['bin/mosaic'],
}

##########################################################################
## Run setup script
##########################################################################

if __name__ == '__main__':
    setup(**config)
