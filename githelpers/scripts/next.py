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
from ..gitlib import children_of_head, is_clean, is_git_repo, reset_hard_to


def _exit_if_not_valid_in_context():
    """
    Exit with return code 2 if the current working directory is not in a Git
    repository or return code 3 if the working directory is dirty. Otherwise,
    return None.
    """
    if not is_git_repo():
        raise ExecutionError(
            'Not in a Git repository.\nAborting.', 2
        )

    if not is_clean():
        raise ExecutionError(
            'Workspace contains uncommitted changes.\nAborting.', 3
        )


def _child():
    """
    Return the SHA1 hash of the single child commit of HEAD. Exit with return
    code 4 if there is no child commit (HEAD is at the "tip" of a branch).
    Exit with return code 5 if HEAD has more than one child commit.
    """
    child_sha1s = children_of_head()

    if len(child_sha1s) == 0:
        raise ExecutionError(
            'No next commit.\a', 4
        )

    if len(child_sha1s) > 1:
        raise ExecutionError(
            'More than one child.\nAborting.\a', 5
        )

    return child_sha1s[0]


def _next():
    """
    Move the current branch (upward) to its immediate child. Exits with an
    error message if there is not exactly one direct child or if changes in
    the working directory would be lost.
    """
    _exit_if_not_valid_in_context()
    reset_hard_to(_child())


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
