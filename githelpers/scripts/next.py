# encoding: utf-8

"""
Move the current branch (upward) to its immediate child. Exits with an error
message if there is not exactly one direct child or if changes in the working
directory would be lost.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys

from .exceptions import ExecutionError


def _next():
    """
    Move the current branch (upward) to its immediate child. Exits with an
    error message if there is not exactly one direct child or if changes in
    the working directory would be lost.
    """
    raise NotImplementedError


def main():
    """
    Entry point for 'next' script.
    """
    try:
        _next()
    except ExecutionError as e:
        print(e.message, file=sys.stderr)
        return e.return_code
    return 0
