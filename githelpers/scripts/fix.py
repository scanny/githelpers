# encoding: utf-8

"""
Move 'fixit' branch to the commit identified by sys.argv[1]. Exits with an
error message if the current working directory is not in a Git repository,
the working tree is dirty, or *commit_ref* does not identify a commit in the
repository.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys

from .exceptions import ExecutionError
from ..gitlib import is_clean, is_git_repo


def _exit_if_not_valid_in_context():
    """
    Exit with an error message if the current working directory is not in a Git
    repository or if the working directory is dirty. Otherwise, return None.
    """
    if not is_git_repo():
        raise ExecutionError(
            'Not in a Git repository.\nAborting.', 2
        )

    if not is_clean():
        raise ExecutionError(
            'Workspace contains uncommitted changes.\nAborting.', 3
        )


def _exit_if_not_valid(commit_ref):
    """
    Exit with an error message if *commit_ref* does not identify a commit in
    the repository. Otherwise, return None.
    """
    raise NotImplementedError


def _checkout_branch_and_reset_to(branch_name, commit_ref):
    """
    Check out *branch_name* and reset it hard to *commit_ref*. Create the
    branch at HEAD it doesn't exist.
    """
    raise NotImplementedError


def _fix(commit_ref):
    """
    Move 'fixit' branch to the commit identified by *commit_ref*. Exits with
    an error message if the current working directory is not in a Git
    repository or if *commit_ref* does not identify a commit in the
    repository.
    """
    _exit_if_not_valid_in_context()
    _exit_if_not_valid(commit_ref)
    _checkout_branch_and_reset_to('fixit', commit_ref)


def main(argv=None):
    """
    Entry point for 'fix' script.
    """
    commit_ish = sys.argv[1] if argv is None else argv[1]
    try:
        _fix(commit_ish)
    except ExecutionError as e:
        print(e.message, file=sys.stderr)
        return e.return_code
    return 0
