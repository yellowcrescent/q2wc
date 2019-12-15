#!/usr/bin/env python3
# pylint: disable=W,C

from setuptools import setup, find_packages
setup(
    name = "q2wc",
    version = "0.1.0",
    author = "Jacob Hipps",
    author_email = "jacob@ycnrg.org",
    license = "MIT",
    description = "Quixel to World Creator 2",
    keywords = "world-creator quixel megascans convert texture surface",
    url = "https://git.ycnrg.org/projects/BPY/repos/q2wc/",

    packages = find_packages(),
    scripts = [],

    install_requires = [],

    package_data = {
        '': [ '*.md' ],
    },

    entry_points = {
        'console_scripts': [ 'q2wc = q2wc:_main' ]
    }

    # could also include long_description, download_url, classifiers, etc.
)
