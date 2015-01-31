# encoding: utf-8

"""
Acceptance test step implementations related to repository.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from behave import given, then, when

import githelpers.scripts.fix as fix
import githelpers.scripts.next as next
import githelpers.scripts.prev as prev
import githelpers.scripts.drop as drop

from githelpers.gitlib import (
    checkout, current_branch_name, head, is_reachable, reset_hard_to
)


# given ===================================================

@given('rev {abbrev} is reachable')
def given_rev_abbrev_is_reachable(context, abbrev):
    assert is_reachable(abbrev)


@given('the current branch is \'{branch_name}\'')
def given_the_current_branch_is_branch_name(context, branch_name):
    if current_branch_name() != branch_name:
        checkout(branch_name)


@given('the current commit is {sha1}')
def given_the_current_commit_is_sha1(context, sha1):
    reset_hard_to(sha1)


@given('the working directory is a Git repo')
def given_the_cwd_is_a_Git_repository(context):
    context.repo_dir.chdir()


@given('the working directory is not in a Git repository')
def given_the_cwd_is_not_in_a_Git_repository(context):
    context.empty_dir.chdir()


@given('the working tree is not clean')
def given_the_working_tree_is_not_clean(context):
    with open('barbaz.txt', 'w') as f:
        f.write('barbazzle\n')


# when ====================================================

@when('I issue the command `fix {commit_ish}`')
def when_I_issue_the_command_fix_commit_ish(context, commit_ish):
    rc = fix.main(['behave-fix', commit_ish])
    context.return_code = rc


@when('I issue the command `next`')
def when_I_issue_the_command_next(context):
    context.return_code = next.main()


@when('I issue the command `prev`')
def when_I_issue_the_command_prev(context):
    context.return_code = prev.main()


@when('I issue the command `drop {abbrev}`')
def when_I_issue_the_command_drop_abbrev(context, abbrev):
    rc = drop.main(['behave-drop', abbrev])
    context.return_code = rc


# then ====================================================

@then('HEAD is {abbrev_hash}')
def then_HEAD_is_abbrev_hash(context, abbrev_hash):
    assert head().startswith(abbrev_hash)


@then('rev {abbrev} is not reachable')
def then_rev_abbrev_is_not_reachable(context, abbrev):
    assert not is_reachable(abbrev)


@then('the current branch is \'{branch_name}\'')
def then_the_current_branch_is_branch_name(context, branch_name):
    branch = current_branch_name()
    assert branch == branch_name, "got '%s'" % branch


@then('the return code is {return_code}')
def then_the_return_code_is_return_code(context, return_code):
    rc = context.return_code
    assert rc == int(return_code), 'got %d' % rc


@then('stderr output starts with \'{prefix}\'')
def then_stderr_output_starts_with_prefix(context, prefix):
    err = context.stderr_capture.getvalue()
    assert err.startswith(prefix), 'got:\n\'%s\'' % err
