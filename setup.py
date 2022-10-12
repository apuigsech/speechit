#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

NAME = 'speechit'
DESCRIPTION = ''
URL = 'https://github.com/apuigsech/speechit'
EMAIL = 'albert@puigsech.com'
AUTHOR = 'Albert Puigsech'
REQUIRES_PYTHON = '>=3.9.0'
VERSION = None
LICENSE = 'MIT'
REQUIRED = []

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['speechit'],
    entry_points={
        'console_scripts': ['speechit=speechit:main'],
    },
    data_files=[('etc/speechit', ['default.conf'])],
    install_requires=REQUIRED,
    license=LICENSE,
    project_urls={ 
        'Bug Reports': 'https://github.com/apuigsech/speechit/issues',
        'Source': 'https://github.com/apuigsech/speechit',
    },
)
