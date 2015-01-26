# encoding: utf-8

"""
Unit test suite for the githelpers module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from zipfile import ZipFile

import py
import pytest

from githelpers.gitlib import branch_names, checkout, current_branch_name


TEST_REPO_ZIP = str(py.path.local(__file__).dirpath('test-repo.zip'))


class Describe_branch_names(object):

    def it_returns_all_the_local_branch_names(self, readonly_test_repo):
        assert branch_names() == [
            'feature/foobar', 'fixit', 'master', 'spike'
        ]


class Describe_checkout(object):

    def it_checks_out_a_branch(self, new_test_repo):
        bazfoo = new_test_repo.join('bazfoo.txt')
        assert not bazfoo.check()
        checkout('master')
        assert bazfoo.check()
        assert current_branch_name() == 'master'


class Describe_current_branch_name(object):

    def it_is_spike_for_test_repo(self, readonly_test_repo):
        assert current_branch_name() == 'spike'


# shared fixtures ----------------------------------------------------

@pytest.fixture(scope='module')
def module_test_repo(request):
    """
    Extract the test repo into a temporary directory having module scope.
    """
    test_repo_dir = py.test.ensuretemp('test-repo')
    zip_file = ZipFile(TEST_REPO_ZIP)
    zip_file.extractall(str(test_repo_dir))
    return test_repo_dir


@pytest.fixture
def readonly_test_repo(request, module_test_repo):
    """
    Change the current working directory to the module scope test repo,
    restoring the original working directory after the test.
    """
    cwd = module_test_repo.chdir()
    request.addfinalizer(lambda: cwd.chdir())


@pytest.fixture
def new_test_repo(request, tmpdir):
    """
    Extract the test repo into a temporary directory, making that temp
    directory the current working directory. Restore the original current
    working directory after request.
    """
    test_repo_dir = tmpdir.mkdir("test-repo")
    zip_file = ZipFile(TEST_REPO_ZIP)
    zip_file.extractall(str(test_repo_dir))
    cwd = test_repo_dir.chdir()
    request.addfinalizer(lambda: cwd.chdir())
    return test_repo_dir
