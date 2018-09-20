# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os


long_description = """
idephyx = Interface for Distributed Ephys eXperiment

It is a neural recorder system for multi electrode with real time spike sorting and distributed facilities.

It is front end based on pyacq and tridesclous.

It can be used with device supported by pyacq (National Instrument, Measurement comuting,
Blackrock, MultiChannelSystem, ...)


"""

d = {}
exec(open("idephyx/version.py").read(), None, d)
version = d['version']



setup(
    name = "idephyx",
    version = version,
    packages = [pkg for pkg in find_packages() if pkg.startswith('idephyx')],
    install_requires=[
                    'pyqtgraph',
                    'pyacq',
                    'tridesclous',
                    'ephyviewer',
                    'psutil',
                    ],
    author = "S.Garcia",
    author_email = "sam.garcia.die@gmail.com",
    description = "Interface for Distributed Ephys eXperiment",
    long_description = long_description,
    license = "MIT",
    url='https://github.com/samuelgarcia/idephyx',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering'],
    entry_points={
          'console_scripts': ['idephyx=idephyx.script:main'],
        },
    
)
