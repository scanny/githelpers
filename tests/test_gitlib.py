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

from githelpers.gitlib import (
    branch_names, checkout, current_branch_name, is_clean, is_commit,
    is_git_repo
)


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


class Describe_is_clean(object):

    def it_returns_True_in_clean_repo(self, clean_repo_fixture):
        assert is_clean() is True

    def it_returns_False_in_dirty_repo(self, dirty_repo_fixture):
        assert is_clean() is False

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def clean_repo_fixture(self, request, readonly_test_repo):
        pass

    @pytest.fixture
    def dirty_repo_fixture(self, request, new_test_repo):
        new_test_repo.join('newfile.txt').write('0x984rt\n')


class Describe_is_commit(object):

    def it_is_True_for_commit(self, valid_sha1_fixture):
        sha1 = valid_sha1_fixture
        assert is_commit(sha1) is True

    def it_is_False_for_nonexistent_sha1(self, bad_hash_fixture):
        sha1 = bad_hash_fixture
        assert is_commit(sha1) is False

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def valid_sha1_fixture(self, request, readonly_test_repo):
        return '6604de21f566378d994a517018a909c078a055bc'

    @pytest.fixture
    def bad_hash_fixture(self, request, readonly_test_repo):
        return 'f00ba59999999999999999999999999999999999'


class Describe_is_git_repo(object):

    def it_returns_True_in_git_repo(self, inside_repo_fixture):
        assert is_git_repo() is True

    def it_returns_False_outside_git_repo(self, outside_repo_fixture):
        assert is_git_repo() is False

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def inside_repo_fixture(self, request, readonly_test_repo):
        return

    @pytest.fixture
    def outside_repo_fixture(self, request, tmpdir):
        non_repo_dir = tmpdir.mkdir("not-a-git-repo")
        cwd = non_repo_dir.chdir()
        request.addfinalizer(lambda: cwd.chdir())


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
