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
from ..gitlib import parent_revs_of, reset_hard_to


def _exit_if_not_valid_in_context():
    """
    Exit with an error message if the current working directory is not in
    a Git repository, the working directory is dirty, or the current branch
    is independent. Otherwise, return |None|.
    """
    pass


def _parent():
    """
    Return the SHA1 hash of the first parent commit of HEAD. Exit with an
    error message if there is no parent commit (i.e. HEAD is an initial
    commit).
    """
    parents = parent_revs_of('HEAD')
    if not parents:
        raise ExecutionError('No parent commit.\nAborting.\a', 5)
    return parents[0]


def _prev():
    """
    Move the current branch (downward) to its parent commit. Exits with an
    error message if changes in the working directory would be lost or if the
    current commit would no longer be reachable.
    """
    _exit_if_not_valid_in_context()
    reset_hard_to(_parent())


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
