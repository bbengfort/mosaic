# Mosaic

**User space file system usage analysis tool.**

[![Build Status](https://travis-ci.org/bbengfort/mosaic.svg?branch=master)](https://travis-ci.org/bbengfort/mosaic)
[![Coverage Status](https://coveralls.io/repos/bbengfort/mosaic/badge.svg?branch=master&service=github)](https://coveralls.io/github/bbengfort/mosaic?branch=master)
[![Stories in Ready](https://badge.waffle.io/bbengfort/mosaic.png?label=ready&title=Ready)](https://waffle.io/bbengfort/mosaic)

[![Buenos Aires (Emirates Air-Line campaign)][buenos_aires.jpg]][buenos_aires_flickr]

## Getting Started

The simplest way to install the mosaic tools is to use the `setup.py` script included with this repository as follows:

    $ python setup.py install

This will install our file system analysis library to your Python site-pacakges as well as install a `mosaic` utility into your path. Of course you can also follow the development instructions below. In order to run a file system usage analysis on your home directory, use the `mosaic` utility as follows:

    $ mosaic usage ~

This will recursively walk your home directory, counting different objects, and will write the analysis data structure to your current working directory.

## Development

Here are the brief instructions for getting this thing set up for development. First clone the repository and switch directories into it:

    $ git clone git@github.com:bbengfort/mosaic.git
    $ cd mosaic

Note that you may need to fork this repository on Github into your own repository (and we will definitely accept pull requests). At this point you should set up your virtual environment. If you don't have `virtualenv` and `virtualenvwrapper` installed, please figure out how to set that up and configure it. Create the virtual environment and install the dependencies as follows. With `virtualenvwrapper`:

    $ mkvirtualenv -a $(pwd) -r requirements.txt mosaic

And with `virtualenv` alone:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt

You should also add the mosaic package to your Python path. There are several ways to do this, my favorite is to export a `.pth` file into the site-packages directory of the virtualenv. (I also tend to add the `bin/` directory to the virtualenv ``$PATH` as well).

At this point you should be able to run the tests and have them pass:

    (mosaic)$ make test

Now it's time to switch into the development branch:

    (mosaic)$ git checkout origin develop

And you can get started using the contribution details outlined below!

### Contributing

Our file system usage analysis utility and library is open source, but because this is a University of Maryland project, we would appreciate it if you would let us know how you intend to use the software (other than simply copying and pasting code so that you can use it in your own projects). If you would like to contribute (especially if you are a student at the University of Maryland), you can do so in the following ways:

1. Add issues or bugs to the bug tracker: [https://github.com/bbengfort/mosaic/issues](https://github.com/bbengfort/mosaic/issues)
2. Work on a card on the dev board: [https://waffle.io/bbengfort/mosaic](https://waffle.io/bbengfort/mosaic)
3. Create a pull request in Github: [https://github.com/bbengfort/mosaic/pulls](https://github.com/bbengfort/mosaic/pulls)

Note that labels in the Github issues are defined in the blog post: [How we use labels on GitHub Issues at Mediocre Laboratories](https://mediocre.com/forum/topics/how-we-use-labels-on-github-issues-at-mediocre-laboratories).

If you've contributed a fair amount, I'll give you direct access to the repository, which is set up in a typical production/release/development cycle as described in _[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)_. A typical workflow is as follows:

1. Select a card from the [dev board](https://waffle.io/bbengfort/mosaic) - preferably one that is "ready" then move it to "in-progress".

2. Create a branch off of develop called "feature-[feature name]", work and commit into that branch.

        ~$ git checkout -b feature-myfeature develop

3. Once you are done working (and everything is tested) merge your feature into develop.

        ~$ git checkout develop
        ~$ git merge --no-ff feature-myfeature
        ~$ git branch -d feature-myfeature
        ~$ git push origin develop

4. Repeat. Releases will be routinely pushed into master via release branches, then deployed to the server.

Note that pull requests will be reviewed when the Travis-CI tests pass, so including tests with your pull request is ideal!

## About

Part of my study of distributed file systems requires understanding what is on those file systems. Mosaic is a tool for performing that analysis.

### Attribution

The photo used in this README, [Buenos Aires (Emirates Air-Line campaign)][buenos_aires_flickr] by [Charis Tsevis](https://www.flickr.com/photos/tsevis/) is used under a [CC BY-NC-ND 2.0](https://creativecommons.org/licenses/by-nc-nd/2.0/) creative commons license.

[buenos_aires.jpg]: docs/images/buenos_aires.jpg
[buenos_aires_flickr]: https://flic.kr/p/oCAg4Q
