# encoding: utf-8

"""Setup and teardown logic for scenarios."""

import os
import tempfile

from zipfile import ZipFile

import py


def before_scenario(context, scenario):
    """Initialize fresh copy of the test repository in temp directory.

    Store the test-respository directory in `context.repo_dir`. Also store the current
    working directory in `context.original_working_dir` so it can be restored after the
    feature is run.
    """
    test_repo_dir = py.path.local(tempfile.mkdtemp())
    empty_dir = py.path.local(tempfile.mkdtemp())

    if "linear-repo" in scenario.tags:
        repo_zip = _test_file("linear-repo.zip")
    else:
        repo_zip = _test_file("test-repo.zip")

    zip_file = ZipFile(repo_zip)
    zip_file.extractall(str(test_repo_dir))

    context.original_working_dir = test_repo_dir.chdir()
    context.repo_dir, context.empty_dir = test_repo_dir, empty_dir


def after_scenario(context, scenario):
    """Restore original working directory and remove test-repo temp-directory."""
    context.original_working_dir.chdir()
    context.repo_dir.remove(rec=1)
    context.empty_dir.remove(rec=1)


def _test_file(filename):
    """Return str absolute path to *filename* in acceptance test_files directory."""
    thisdir = os.path.split(__file__)[0]
    return os.path.abspath(os.path.join(thisdir, "steps", "test_files", filename))
