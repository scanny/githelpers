# encoding: utf-8

"""
Git helper functions, each roughly equivalent to a form of a git command.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .runcmd import output_of, return_code_of
from .runcmd import RunCmdError  # noqa


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


def branch_hashes():
    """
    Return a list containing the SHA1 hash for each of the local branches in
    this repository.
    """
    out = output_of(['git', 'show-ref', '--heads', '--hash'])
    return [line for line in out.splitlines()]


def branch_names():
    """
    Return a list containing the branch name of each local branch in this
    repository.
    """
    out = output_of(
        ['git', 'for-each-ref', '--format=%(refname)', 'refs/heads']
    )
    return [line[11:] for line in out.splitlines()]


def branches_containing(commitish):
    """
    Return a list containing the name of each local branch from which
    *commitish* is reachable.
    """
    raise NotImplementedError


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


def full_hash_of(commit_ish):
    """
    Return the full 40-character SHA1 hash digest of the commit identified by
    *commit_ish*. Raises |RunCmdError| if *commit_ish* does not correspond to
    a revision in the repository.
    """
    return output_of(['git', 'rev-parse', commit_ish]).strip()


def head():
    """
    Return the SHA1 hash of the commit pointed to by 'HEAD'.
    """
    return output_of(['git', 'rev-parse', 'HEAD']).strip()


def head_is_independent():
    """
    Return |True| if the current commit would become unreachable if the
    current branch pointer was moved "downward" to the parent commit. |False|
    otherwise.
    """
    return head() in independent_branch_hashes()


def independent_branch_hashes():
    """
    Return a list containing the SHA1 hash for each local branch that cannot
    be reached from another branch. Conceptually, an independent branch is
    a commit graph "tip" that has only one branch reference.
    """
    out = output_of(
        ['git', 'show-branch', '--independent'] + branch_hashes()
    )
    return [line for line in out.splitlines()]


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


def is_reachable(commitish):
    """
    Return |True| if the commit idenfied by *commitish* is reachable from at
    least one branch.
    """
    return full_hash_of(commitish) in reachable_revs()


def parent_revs_of(commitish):
    """
    Return a list containing the SHA1 hash of each commit that is a parent of
    *commitish*.
    """
    rev = full_hash_of(commitish)
    parents_spec = '%s^@' % rev
    return output_of(['git', 'rev-parse', parents_spec]).split()


def reachable_revs():
    """
    Return a list of revs corresponding to the commits that can be reached
    from one of the repository refs, including local, remote, and tag refs.
    """
    return output_of(['git', 'rev-list', '--all']).split()


def rebase_onto(newbase, fork_point, branch_name):
    """
    Rebase *branch_name* onto *newbase* up to but not including the commit at
    *fork_point*.
    """
    raise NotImplementedError


def reset_hard_to(commit_ref):
    """
    Move the current branch to *commit_ref*, modifying the working tree to
    match that commit.
    """
    return output_of(['git', 'reset', '--hard', commit_ref])
