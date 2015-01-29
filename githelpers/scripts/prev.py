# encoding: utf-8

"""
Move the current branch (downward) to its parent commit. Exits with an error
message if changes in the working directory would be lost or if the current
commit would no longer be reachable.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys

from .exceptions import ExecutionError


def _prev():
    """
    Move the current branch (downward) to its parent commit. Exits with an
    error message if changes in the working directory would be lost or if the
    current commit would no longer be reachable.
    """
    raise NotImplementedError


def main():
    """
    Entry point for 'prev' script.
    """
    try:
        _prev()
    except ExecutionError as e:
        print(e.message, file=sys.stderr)
        return e.return_code
    return 0
