from __future__ import with_statement

import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup

import os
with open(os.path.join(os.path.dirname(__file__),"README.rst"), 'r') as fh:
    long_desc = fh.read()

VERSION = "0.1"

setup(name="dedupe",
      version=VERSION,
      description="A thing to detect duplicate music",
      long_description=long_desc,
      author="Brandon W Maister",
      author_email="quodlibetor@gmail.com",
      url="http://bitbucket.org/quodlibetor/dedupe",
      entry_points= {'console_scripts': [
            'dedupe = dedupe:main'
            ]},
      install_requires=['mutagen', 'argparse'],
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5", # min
        "Operating System :: OS Independent",  # I think?
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (LGPL)",
        "Operating System :: OS Independent",
        ]
      )
