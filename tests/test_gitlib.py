# encoding: utf-8

"""Unit test suite for the githelpers module."""

from zipfile import ZipFile

import py
import pytest

from githelpers.gitlib import (
    branch_exists,
    branch_hash,
    branch_hashes,
    branch_names,
    branches_containing,
    checkout,
    children_of_head,
    create_branch_at,
    current_branch_name,
    delete_branch,
    head,
    head_is_independent,
    independent_branch_hashes,
    is_clean,
    is_commit,
    is_git_repo,
    parent_revs_of,
    reset_hard_to,
)


TEST_REPO_ZIP = str(py.path.local(__file__).dirpath("test-repo.zip"))


class Describe_branch_exists(object):
    def it_is_True_for_existing_branch(self, readonly_test_repo):
        assert branch_exists("master") is True

    def it_is_False_for_nonexistent_branch(self, readonly_test_repo):
        assert branch_exists("fzxyed") is False


class Describe_branch_hashes(object):
    def it_returns_a_hash_for_each_branch(self, call_fixture):
        expected_value = call_fixture
        hashes = branch_hashes()
        assert hashes == expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def call_fixture(self, readonly_test_repo):
        return [
            "27caec118c2fa2a11b481a02e68a214a64cb3e87",
            "0eafe04e11a41374a1bd11f2eb1776d9d44febb1",
            "53a12abad9779cd3c4b02b83df01af9c01ed28b4",
            "2294d9797588a8a0f6aa95ef488cf872b36f2131",
        ]


class Describe_branch_names(object):
    def it_returns_all_the_local_branch_names(self, readonly_test_repo):
        assert branch_names() == ["feature/foobar", "fixit", "master", "spike"]


class Describe_branches_containing(object):
    def it_returns_branch_names_containing_commitish(self, call_fixture):
        commitish, expected_value = call_fixture
        branch_names = branches_containing(commitish)
        assert branch_names == expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("2294d97", ["spike"]),
            ("27caec1", ["feature/foobar", "master"]),
            ("99ec480", ["feature/foobar", "master", "spike"]),
            ("0eafe04", ["feature/foobar", "fixit", "master", "spike"]),
        ]
    )
    def call_fixture(self, request, readonly_test_repo):
        commitish, branch_names = request.param
        return commitish, branch_names


class Describe_checkout(object):
    def it_checks_out_a_branch(self, new_test_repo):
        bazfoo = new_test_repo.join("bazfoo.txt")
        assert not bazfoo.check()
        checkout("master")
        assert bazfoo.check()
        assert current_branch_name() == "master"


class Describe_children_of_head(object):
    def it_returns_the_child_commit_hashes(self, call_fixture):
        expected_value = call_fixture
        hashes = children_of_head()
        assert hashes == expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("spike", []),
            ("fixit", ["6604de21f566378d994a517018a909c078a055bc"]),
            (
                "99ec480",
                [
                    "27caec118c2fa2a11b481a02e68a214a64cb3e87",
                    "2294d9797588a8a0f6aa95ef488cf872b36f2131",
                ],
            ),
        ]
    )
    def call_fixture(self, request, new_test_repo):
        commit_ish, hashes = request.param
        checkout(commit_ish)
        return hashes


class Describe_create_branch_at(object):
    def it_creates_a_new_branch_at_commit_ref(self, new_test_repo):
        assert not branch_exists("foobar")

        create_branch_at("foobar", "2294d979")

        assert branch_exists("foobar")
        assert branch_hash("foobar").startswith("2294d979")
        assert current_branch_name() != "foobar"


class Describe_current_branch_name(object):
    def it_is_spike_for_test_repo(self, readonly_test_repo):
        assert current_branch_name() == "spike"


class Describe_delete_branch(object):
    def it_removes_a_branch(self, new_test_repo):
        assert branch_exists("feature/foobar")
        delete_branch("feature/foobar")
        assert not branch_exists("feature/foobar")

    def it_raises_on_delete_current_branch(self, new_test_repo):
        with pytest.raises(ValueError):
            delete_branch("spike")


class Describe_head_is_independent(object):
    def it_knows_whether_current_branch_is_independent(self, call_fixture):
        expected_value = call_fixture
        assert head_is_independent() == expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("spike", True),
            ("master", True),
            ("feature/foobar", False),
            ("fixit", False),
        ]
    )
    def call_fixture(self, request, new_test_repo):
        branch_name, expected_value = request.param
        checkout(branch_name)
        return expected_value


class Describe_independent_branch_hashes(object):
    def it_returns_a_hash_for_each_independent_branch(self, call_fixture):
        expected_value = call_fixture
        hashes = independent_branch_hashes()
        assert hashes == expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def call_fixture(self, readonly_test_repo):
        return [
            "53a12abad9779cd3c4b02b83df01af9c01ed28b4",
            "2294d9797588a8a0f6aa95ef488cf872b36f2131",
        ]


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
        new_test_repo.join("newfile.txt").write("0x984rt\n")


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
        return "6604de21f566378d994a517018a909c078a055bc"

    @pytest.fixture
    def bad_hash_fixture(self, request, readonly_test_repo):
        return "f00ba59999999999999999999999999999999999"


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


class Describe_parent_revs_of(object):
    def it_returns_a_hash_for_each_parent_commit(self, call_fixture):
        commitish, expected_value = call_fixture
        revs = parent_revs_of(commitish)
        assert revs == expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("spike", ["99ec48014b47dc9f9cfe6fd325b281dbaed12d3f"]),
            ("fixit", []),
            ("master", ["27caec118c2fa2a11b481a02e68a214a64cb3e87"]),
            ("HEAD", ["99ec48014b47dc9f9cfe6fd325b281dbaed12d3f"]),
        ]
    )
    def call_fixture(self, request, new_test_repo):
        commitish, revs = request.param
        return commitish, revs


class Describe_reset_hard_to(object):
    def it_resets_the_commit_and_working_tree(self, new_test_repo):
        barbaz = new_test_repo.join("barbaz.txt")
        assert barbaz.check()
        reset_hard_to("fixit")
        assert not barbaz.check()
        assert head() == "0eafe04e11a41374a1bd11f2eb1776d9d44febb1"


# shared fixtures ----------------------------------------------------


@pytest.fixture(scope="module")
def module_test_repo(request, tmpdir_factory):
    """Extract the test repo into a temporary directory having module scope."""
    test_repo_dir = tmpdir_factory.mktemp("test-repo")
    ZipFile(TEST_REPO_ZIP).extractall(str(test_repo_dir))
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
