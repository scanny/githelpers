# encoding: utf-8

"""Remove a commit from its branch.

Exits with an error message if the commit is reachable from more than one local branch
or has other than one parent commit.
"""

import sys
from typing import List, Optional

from .exceptions import ExecutionError
from ..gitlib import (
    branches_containing,
    checkout,
    current_branch_name,
    full_hash_of,
    is_clean,
    is_git_repo,
    is_reachable,
    parent_revs_of,
    rebase_onto,
)
from ..runcmd import RunCmdError


def main(argv: Optional[List[str]] = None):
    """Entry point for 'drop' script."""
    args = sys.argv[1:] if argv is None else argv[1:]
    if len(args) != 1:
        print("usage: drop <commit>")
        return 1

    commitish = args[0]

    try:
        _drop(commitish)
    except ExecutionError as e:
        print(e.message, file=sys.stderr)
        return e.return_code
    return 0


def _drop(commitish_to_drop: str):
    """Remove `commitish_to_drop` from its branch.

    Exits with an error message if `commitish_to_drop` is reachable from more than one
    branch or has other than exactly one parent.
    """
    _exit_if_not_valid_in_context(commitish_to_drop)

    rev_to_drop = _resolve_rev(commitish_to_drop)
    orig_branch = current_branch_name()
    commit_branch = _only_branch_containing(commitish_to_drop)
    newbase = _single_parent_of(commitish_to_drop)

    print(rebase_onto(newbase, rev_to_drop, commit_branch))

    if current_branch_name() != orig_branch and orig_branch != "HEAD":
        checkout(orig_branch)


def _exit_if_not_valid_in_context(commitish: str):
    """Exit with error message when current state does not permit drop.

    These conditions are:

    * the current working directory is not in a Git repository
    * the working directory is dirty
    * the current branch is independent

    """
    if not is_git_repo():
        raise ExecutionError("Not in a Git repository.\nAborting.", 2)

    # --- raise if `commitish` is not a revision in repo ---
    _resolve_rev(commitish)

    if not is_clean():
        raise ExecutionError("Workspace contains uncommitted changes.\nAborting.\a", 3)


def _only_branch_containing(commitish: str):
    """Return the name of the branch containing `commitish`.

    Exit with an error message if `commitish` can be reached from other than exactly one
    branch.
    """
    branch_names = branches_containing(commitish)
    branch_count = len(branch_names)

    if branch_count > 1:
        raise ExecutionError(
            "Commit %s reachable from more than one branch.\n" "Aborting." % commitish,
            5,
        )

    return branch_names[0]


def _resolve_rev(commitish: str):
    """Return the 40 character SHA1 hash for `committish`.

    Exit with an error message if `commitish` does not resolve to a reachable commit in
    the repository.
    """
    try:
        rev = full_hash_of(commitish)
    except RunCmdError:
        raise ExecutionError("Unknown revision %s.\a" % commitish, 4)

    if not is_reachable(rev):
        raise ExecutionError(
            "%s is not a reachable commit.\nAborting.\a" % commitish, 4
        )

    return rev


def _single_parent_of(commitish: str):
    """Return the SHA1 hash of the single parent of `commitish`.

    Exit with an error message if there is other than a single parent.
    """
    parent_revs = parent_revs_of(commitish)
    parent_rev_count = len(parent_revs)

    if parent_rev_count == 0:
        raise ExecutionError("Commit %s has no parent.\nAborting.\a" % commitish, 6)

    if parent_rev_count > 1:
        raise ExecutionError(
            "Commit %s has more than one parent.\nAborting." % commitish, 7
        )

    return parent_revs[0]
