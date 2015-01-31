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
from ..gitlib import (
    branches_containing, checkout, current_branch_name, full_hash_of,
    is_reachable, parent_revs_of, rebase_onto, RunCmdError
)


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
    branch_names = branches_containing(commitish)
    branch_count = len(branch_names)

    if branch_count > 1:
        raise ExecutionError(
            'Commit %s reachable from more than one branch.\n'
            'Aborting.' % commitish, 5
        )

    return branch_names[0]


def _resolve_rev(commitish):
    """
    Return the 40 character SHA1 hash for *committish*. Exit with an error
    message if *commitish* does not resolve to a reachable commit in the
    repository.
    """
    try:
        rev = full_hash_of(commitish)
    except RunCmdError:
        raise ExecutionError(
            'Unknown revision %s.\a' % commitish, 4
        )

    if not is_reachable(rev):
        raise ExecutionError(
            '%s is not a reachable commit.\nAborting.\a' % commitish, 4
        )

    return rev


def _single_parent_of(commitish):
    """
    Return the SHA1 hash of the single parent of *commitish*. Exit with an
    error message if there is other than a single parent.
    """
    parent_revs = parent_revs_of(commitish)
    parent_rev_count = len(parent_revs)

    if parent_rev_count == 0:
        raise ExecutionError(
            'Commit %s has no parent.\nAborting.\a' % commitish, 6
        )

    if parent_rev_count > 1:
        raise ExecutionError(
            'Commit %s has more than one parent.\nAborting.' % commitish, 7
        )

    return parent_revs[0]


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
