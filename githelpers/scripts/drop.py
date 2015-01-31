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
from ..gitlib import checkout, current_branch_name, rebase_onto


def _exit_if_not_valid_in_context():
    """
    Exit with an error message if the current working directory is not in
    a Git repository, the working directory is dirty, or the current branch
    is independent.
    """
    pass


def _only_branch_containing(commitish):
    """
    Return the name of the branch containing *commitish*. Exit with an error
    message if *commitish* can be reached from other than exactly one branch.
    """
    raise NotImplementedError


def _resolve_rev(commitish):
    """
    Return the 40 character SHA1 hash for *committish*. Exit with an error
    message if *commitish* does not resolve to a reachable commit in the
    repository.
    """
    raise NotImplementedError


def _single_parent_of(commitish):
    """
    Return the SHA1 hash of the single parent of *commitish*. Exit with an
    error message if there is other than a single parent.
    """
    raise NotImplementedError


def _drop(commitish_to_drop):
    """
    Remove *commitish_to_drop* from its branch. Exits with an error message
    if *commitish_to_drop* is reachable from more than one branch or has
    other than exactly one parent.
    """
    _exit_if_not_valid_in_context()

    rev_to_drop = _resolve_rev(commitish_to_drop)
    orig_branch = current_branch_name()
    commit_branch = _only_branch_containing(commitish_to_drop)
    newbase = _single_parent_of(commitish_to_drop)

    print(rebase_onto(newbase, rev_to_drop, commit_branch))

    if current_branch_name() != orig_branch and orig_branch != 'HEAD':
        checkout(orig_branch)


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
