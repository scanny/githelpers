# encoding: utf-8

"""
Git helper functions, each roughly equivalent to a form of a git command.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


def branch_names():
    """
    Return a list containing the branch name of each local branch in this
    repository.
    """
    raise NotImplementedError


def checkout(branch_name):
    """
    Checkout branch having *branch_name*.
    """
    raise NotImplementedError


def current_branch_name():
    """
    Return the current branch name, or 'HEAD' if in detached head state.
    """
    raise NotImplementedError


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
