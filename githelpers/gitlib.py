# encoding: utf-8

"""Git helper functions, each roughly equivalent to a form of a git command."""

from .runcmd import output_of, return_code_of
from .runcmd import RunCmdError  # noqa


def branch_exists(branch_name):
    """Return |True| when *branch_name* exists in the current repository."""
    cmd = ["git", "show-ref", "--verify", "refs/heads/%s" % branch_name]
    return return_code_of(cmd) == 0


def branch_hash(branch_name):
    """Return 40-char str SHA1 hash of commit pointed to by *branch_name*."""
    return output_of(["git", "rev-parse", branch_name]).strip()


def branch_hashes():
    """Return list of str SHA1 hash for each of local branch in this repository."""
    out = output_of(["git", "show-ref", "--heads", "--hash"])
    return [line for line in out.splitlines()]


def branch_names():
    """Return list of str name of each local branch in this repository."""
    out = output_of(["git", "for-each-ref", "--format=%(refname)", "refs/heads"])
    return [line[11:] for line in out.splitlines()]


def branches_containing(commitish):
    """Return list of name of each local branch from which *commitish* is reachable."""
    rev = full_hash_of(commitish)
    return [name for name in branch_names() if rev in rev_list(name)]


def checkout(branch_name):
    """Checkout branch having *branch_name*.

    Returns whatever output is send to stdout. Raises |RunCmdError| if checkout is
    unsuccessful.
    """
    return output_of(["git", "checkout", branch_name])


def children_of_head():
    """Return list of str SHA1 hash for each child commit of HEAD."""
    out = output_of(["git", "rev-list", "--all", "--children"])
    head_sha1 = head()
    for line in out.splitlines():
        if line.startswith(head_sha1):
            return line.split()[1:]
    raise Exception("HEAD not found in rev-list output")


def create_branch_at(branch_name, commit_ref):
    """Create branch *branch_name* at *commit_ref*.

    Does not checkout the new branch. Returns stdout output, but this command is
    normally silent.
    """
    return output_of(["git", "branch", branch_name, commit_ref])


def current_branch_name():
    """Return str current branch name, or 'HEAD' if in detached head state."""
    return output_of(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()


def delete_branch(branch_name):
    """Delete the reference refs/heads/{*branch_name*}."""
    if branch_name == current_branch_name():
        raise ValueError("Cannot delete current branch '%s'" % branch_name)
    return output_of(["git", "branch", "-D", branch_name])


def full_hash_of(commit_ish):
    """Return str full 40-character SHA1 hash of commit identified by *commit_ish*.

    Raises |RunCmdError| if *commit_ish* does not correspond to a revision in the
    repository.
    """
    return output_of(["git", "rev-parse", commit_ish]).strip()


def head():
    """Return str SHA1 hash of the commit pointed to by 'HEAD'."""
    return output_of(["git", "rev-parse", "HEAD"]).strip()


def head_is_independent():
    """Return |True| if the current branch pointer is only reference to its commit.

    In this situation, that commit would become unreachable if the current branch
    pointer was moved "downward" to the parent commit. |False| otherwise.
    """
    return head() in independent_branch_hashes()


def independent_branch_hashes():
    """Return list of str SHA1 hash for each independent local branch.

    An independent branch is one that cannot be reached from another branch.
    Conceptually, an independent branch is a commit graph "tip" that has only one branch
    reference.
    """
    out = output_of(["git", "show-branch", "--independent"] + branch_hashes())
    return [line for line in out.splitlines()]


def is_clean():
    """Return |True| when current working directory has no uncommitted changes."""
    out = output_of(["git", "status", "--porcelain"])
    return out == ""


def is_commit(commit_ref):
    """Return |True| when *commit_ref* "points" to a commit in this repository."""
    ref = "%s^{commit}" % commit_ref
    cmd = ["git", "rev-parse", "-q", "--verify", "%s" % ref]
    return return_code_of(cmd) == 0


def is_git_repo():
    """Return |True| when the current working directory is in a git repository."""
    cmd = ["git", "rev-parse", "--git-dir"]
    return return_code_of(cmd) == 0


def is_reachable(commitish):
    """Return |True| when *commitish* is reachable from at least one branch."""
    return full_hash_of(commitish) in reachable_revs()


def parent_revs_of(commitish):
    """Return list of str SHA1 hash of each parent commit of *commitish*."""
    rev = full_hash_of(commitish)
    parents_spec = "%s^@" % rev
    return output_of(["git", "rev-parse", parents_spec]).split()


def reachable_revs():
    """Return list of str SHA1 hash of each commit reachable from a reference.

    All references in the repository are included, including local, remote, and tag
    refs.
    """
    return output_of(["git", "rev-list", "--all"]).split()


def rebase_onto(newbase, fork_point, branch_name):
    """Rebase *branch_name* onto *newbase* exclusive of the commit at *fork_point*."""
    return output_of(
        ["git", "rebase", "--onto", newbase, fork_point, branch_name]
    ).rstrip()


def reset_hard_to(commit_ref):
    """Move current branch to *commit_ref*. Note this is potentially destructive."""
    return output_of(["git", "reset", "--hard", commit_ref])


def rev_list(commitish):
    """Return list of str SHA1 hash of each commit reachable from *commitish*."""
    return output_of(["git", "rev-list", commitish]).split()
