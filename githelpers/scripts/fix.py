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


def _fix(commit_ref):
    """
    Move 'fixit' branch to the commit identified by *commit_ref*. Exits with
    an error message if the current working directory is not in a Git
    repository or if *commit_ref* does not identify a commit in the
    repository.
    """
    raise NotImplementedError


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
