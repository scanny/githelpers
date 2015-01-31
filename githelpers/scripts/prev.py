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
from ..gitlib import (
    head_is_independent, is_clean, is_git_repo, parent_revs_of, reset_hard_to
)


def _exit_if_not_valid_in_context():
    """
    Exit with an error message if the current working directory is not in
    a Git repository, the working directory is dirty, or the current branch
    is independent. Otherwise, return |None|.
    """
    if not is_git_repo():
        raise ExecutionError(
            'Not in a Git repository.\nAborting.', 2
        )

    if not is_clean():
        raise ExecutionError(
            'Workspace contains uncommitted changes.\nAborting.\a', 3
        )

    if head_is_independent():
        raise ExecutionError(
            'Current commit would become unreachable\nAborting.\a', 4
        )


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
    print(reset_hard_to(_parent()), end='')


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
