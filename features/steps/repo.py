# encoding: utf-8

"""
Acceptance test step implementations related to repository.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from behave import given, then, when

import githelpers.scripts.fix as fix

from githelpers.gitlib import checkout, current_branch_name, head


# given ===================================================

@given('the current branch is \'{branch_name}\'')
def given_the_current_branch_is_branch_name(context, branch_name):
    if current_branch_name() != branch_name:
        checkout(branch_name)


@given('the working directory is a Git repo')
def given_the_cwd_is_a_Git_repository(context):
    context.repo_dir.chdir()


@given('the working directory is not in a Git repository')
def given_the_cwd_is_not_in_a_Git_repository(context):
    context.empty_dir.chdir()


# when ====================================================

@when('I issue the command `fix {commit_ish}`')
def when_I_issue_the_command_fix_commit_ish(context, commit_ish):
    rc = fix.main(['behave-fix', commit_ish])
    context.return_code = rc


# then ====================================================

@then('HEAD is {abbrev_hash}')
def then_HEAD_is_abbrev_hash(context, abbrev_hash):
    assert head().startswith(abbrev_hash)


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
