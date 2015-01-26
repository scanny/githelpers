# encoding: utf-8

"""
Git helper functions, each roughly equivalent to a form of a git command.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .runcmd import output_of


def branch_names():
    """
    Return a list containing the branch name of each local branch in this
    repository.
    """
    raise NotImplementedError


def checkout(branch_name):
    """
    Checkout branch having *branch_name*. Returns stdout output. Raises
    |RunCmdError| if checkout is unsuccessful.
    """
    return output_of(['git', 'checkout', branch_name])


def current_branch_name():
    """
    Return the current branch name, or 'HEAD' if in detached head state.
    """
    return output_of(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()


def delete_branch(branch_name):
    """
    Delete the reference refs/heads/{*branch_name*}.
    """
    raise NotImplementedError


def head():
    """
    Return the SHA1 hash of the commit pointed to by 'HEAD'.
    """
    raise NotImplementedError


def is_clean():
    """
    Return |True| if the current working directory has no uncommitted
    changes, otherwise return |False|.
    """
    raise NotImplementedError
