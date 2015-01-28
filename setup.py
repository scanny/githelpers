#!/usr/bin/env python
# encoding: utf-8

import codecs
import os
import re

from setuptools import setup

MAIN_PKG = 'githelpers'


def _read_from_file(relpath):
    """
    Return the text contained in the file at *relpath* as unicode.
    """
    thisdir = os.path.dirname(__file__)
    path = os.path.join(thisdir, relpath)
    with codecs.open(path, encoding='utf8') as f:
        text = f.read()
    return text


NAME = 'githelpers'

DESCRIPTION = (
    'Provides Git helper scripts such as `next`, `prev`, and `fix`.'
)

KEYWORDS = 'git'
AUTHOR = 'Steve Canny'
AUTHOR_EMAIL = 'stcanny@gmail.com'
URL = 'https://github.com/scanny'

PACKAGES = [MAIN_PKG, 'githelpers.scripts']

ENTRY_POINTS = {
    'console_scripts': [
        'fix = githelpers.scripts.fix:main',
        'next = githelpers.scripts.next:main',
    ]
}


# ---------------------------------------------------------------------------
# Everything below is calculated and shouldn't normally need editing
# ---------------------------------------------------------------------------

# read version from main package __init__.py
init_py = _read_from_file(os.path.join(MAIN_PKG, '__init__.py'))
VERSION = re.search("__version__ = '([^']+)'", init_py).group(1)


params = {
    'author':           AUTHOR,
    'author_email':     AUTHOR_EMAIL,
    'description':      DESCRIPTION,
    'entry_points':     ENTRY_POINTS,
    'keywords':         KEYWORDS,
    'name':             NAME,
    'packages':         PACKAGES,
    'url':              URL,
    'version':          VERSION,
}

setup(**params)
