# encoding: utf-8

"""Wrapper around subprocess, providing command execution services."""

from subprocess import PIPE, Popen
from typing import Sequence, Tuple, Union


Args = Union[Sequence[str], str]


class RunCmdError(Exception):
    """Base class for exceptions in `runcmd` module."""

    def __init__(self, rc: int, cmd: Args, out: bytes, err: bytes):
        self._rc = rc
        self._cmd = cmd
        self._out = out
        self._err = err

    def __str__(self):
        return "Command '%s' returned non-zero exit status %d, reporting:\n%s" % (
            self._cmd,
            self._rc,
            self._err,
        )


def run(args: Args) -> Tuple[int, bytes, bytes]:
    """Return (rc, out, err) 3-tuple indicating result of running the command in *args*.

    *rc*, *out*, and *err* are the return code, output on stdout, and output on stderr,
    respectively.
    """
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    rc = process.returncode
    return rc, out, err


def output_of(args: Args) -> str:
    """Return the output written to stdout by the command line in *args*.

    Raises |RunCmdError| if the return code is not zero.
    """
    rc, out, err = run(args)
    if rc != 0:
        raise RunCmdError(rc, args, out, err)
    return str(out, encoding="utf-8")


def return_code_of(args: Args) -> int:
    """Return the exit code returned from executing the command line in *args*.

    All stdout and stderr output is suppressed.
    """
    rc, _, _ = run(args)
    return rc
