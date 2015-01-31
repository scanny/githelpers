# encoding: utf-8

"""
Remove a commit from its branch. Exits with an error message if the commit is
reachable from more than one local branch or has other than one parent
commit.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys

from .exceptions import ExecutionError


def _drop(commitish_to_drop):
    """
    Remove *commitish_to_drop* from its branch. Exits with an error message
    if *commitish_to_drop* is reachable from more than one branch or has
    other than exactly one parent.
    """
    raise NotImplementedError


def main(argv=None):
    """
    Entry point for 'drop' script.
    """
    commitish = sys.argv[1] if argv is None else argv[1]
    try:
        _drop(commitish)
    except ExecutionError as e:
        print(e.message, file=sys.stderr)
        return e.return_code
    return 0
