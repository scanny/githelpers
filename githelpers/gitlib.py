# encoding: utf-8

"""
Git helper functions, each roughly equivalent to a form of a git command.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .runcmd import output_of, return_code_of


def branch_exists(branch_name):
    """
    Return |True| if a branch having *branch_name* exists in the current
    repository. |False| otherwise.
    """
    cmd = ['git', 'show-ref', '--verify', 'refs/heads/%s' % branch_name]
    return return_code_of(cmd) == 0


def branch_hash(branch_name):
    """
    Return the SHA1 hash of the commit pointed to by *branch_name*.
    """
    return output_of(['git', 'rev-parse', branch_name]).strip()


def branch_names():
    """
    Return a list containing the branch name of each local branch in this
    repository.
    """
    out = output_of(
        ['git', 'for-each-ref', '--format=%(refname)', 'refs/heads']
    )
    return [line[11:] for line in out.splitlines()]


def checkout(branch_name):
    """
    Checkout branch having *branch_name*. Returns stdout output. Raises
    |RunCmdError| if checkout is unsuccessful.
    """
    return output_of(['git', 'checkout', branch_name])


def children_of_head():
    """
    Return a list containing the SHA1 hash for each child commit of HEAD.
    """
    out = output_of(['git', 'rev-list', '--all', '--children'])
    head_sha1 = head()
    for line in out.splitlines():
        if line.startswith(head_sha1):
            return line.split()[1:]
    raise Exception('HEAD not found in rev-list output')


def create_branch_at(branch_name, commit_ref):
    """
    Create branch *branch_name* at *commit_ref*. Does not checkout the new
    branch. Returns stdout output, but this command is normally silent.
    """
    return output_of(['git', 'branch', branch_name, commit_ref])


def current_branch_name():
    """
    Return the current branch name, or 'HEAD' if in detached head state.
    """
    return output_of(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()


def delete_branch(branch_name):
    """
    Delete the reference refs/heads/{*branch_name*}.
    """
    if branch_name == current_branch_name():
        raise ValueError('Cannot delete current branch \'%s\'' % branch_name)
    return output_of(['git', 'branch', '-D', branch_name])


def head():
    """
    Return the SHA1 hash of the commit pointed to by 'HEAD'.
    """
    return output_of(['git', 'rev-parse', 'HEAD']).strip()


def is_clean():
    """
    Return |True| if the current working directory has no uncommitted
    changes, otherwise return |False|.
    """
    out = output_of(['git', 'status', '--porcelain'])
    return out == ''


def is_commit(commit_ref):
    """
    Return |True| if *commit_ref* is a valid reference to a commit in this
    repository. |False| otherwise.
    """
    ref = '%s^{commit}' % commit_ref
    cmd = ['git', 'rev-parse', '-q', '--verify', '%s' % ref]
    return return_code_of(cmd) == 0


def is_git_repo():
    """
    Return |True| if the current working directory is in a git repository,
    False otherwise.
    """
    cmd = ['git', 'rev-parse', '--git-dir']
    return return_code_of(cmd) == 0


def reset_hard_to(commit_ref):
    """
    Move the current branch to *commit_ref*, modifying the working tree to
    match that commit.
    """
    return output_of(['git', 'reset', '--hard', commit_ref])
