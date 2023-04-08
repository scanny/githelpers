#!/usr/bin/env python

"""Print a nicely colored git log, one commit per line.

Example:

    * 0561b64  (4 days)  build: update travis-ci passing icon (HEAD, master)
    * 1786f2f  (4 days)  release: prepare v0.5.7 release  (tag: v0.5.7)
    * a767f78  (4 days)  docs: add new placeholder features to API docs

The log format uses an ASCII x1f (unit-separator) character '' between each field to
ease parsing it into the required tokens. A '' in the commit subject or other field
will break this (but I've never seen it happen).
"""

from __future__ import print_function

import errno
import re
import subprocess
import sys
from typing import List, Tuple


RED = "\033[31m"
RED_BOLD = "\033[0;31;1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"

REFS_COLOR = BLUE
SHA1_COLOR = YELLOW
TAG_COLOR = CYAN
TIME_COLOR = GREEN


def main():
    # --- Send log lines to stdout one at a time, exiting on broken pipe, such as might
    # --- happen when user quits `git-lawg | less` before all input is read.
    try:
        for line in str(LogLines.load()).splitlines():
            print(line)
    except IOError as e:
        if e.errno != errno.EPIPE:
            raise
        sys.stderr.close()


class LogLines(List["Line"]):
    """Collection of `Line` object for each line in the  git log."""

    def __str__(self):
        """The formatted and ANSI-colored git log as a text string.

        Suitable for dumping to the console. Used as the main text output method.
        """
        max_graf, max_sha1, max_time = self._max_widths
        return "\n".join([line.pretty(max_graf, max_sha1, max_time) for line in self])

    @classmethod
    def load(cls):
        """Return |LogLines| object filled with the results of the git log requested.

        Command-line parameters are passed through to the git log command.
        """
        HASH, TIME, SUBJ, REFS = "%h", "%ar", "%s", "%d"

        fmt = "\x1f%s\x1f%s\x1f%s\x1f%s" % (HASH, TIME, SUBJ, REFS)
        cmd = ["git", "log", "--graph", "--pretty=tformat:%s" % fmt] + sys.argv[1:]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        assert proc.stdout is not None

        return cls(Line.from_text(line) for line in proc.stdout.readlines())

    @property
    def _max_widths(self) -> Tuple[int, int, int]:
        """A (max_graf_width, max_sha1_width, max_time_width) 3-tuple.

        Contains the maximum string length of the graf, sha1, and time fields,
        respectively, across all the lines in this list. This is used to present these
        values in even columns.
        """
        graf_widths, sha1_widths, time_widths = zip(*[line.widths for line in self])
        return (max(graf_widths), max(sha1_widths), max(time_widths))


class Line(object):
    """ A single git log line, broken into five tokens:

    * *graf* - the graphical ancestry line characters
    * *sha1* - the commit SHA1 hash
    * *time* - the relative time since the commit, e.g. '2 days'
    * *subj* - the commit message, subject line only
    * *refs* - the REFS string if present, e.g. '(HEAD, master)'

    Handles all the ANSI coloring and line formatting.
    """

    months_regex = re.compile(r", [0-9]+ months?")
    ansi_regex = re.compile(r"\033\[[0-9;]*m")

    def __init__(self, graf: str, sha1: str, time: str, subj: str, refs: str):
        self._graf = graf
        self._sha1 = sha1
        self._time = time
        self._subj = subj
        self._refs = refs

    @classmethod
    def from_text(cls, line: str) -> "Line":
        """Factory method.

        Return a `_Line` object initialized from the raw log line text in `line`.
        """
        tokens = cls._condition(line).split("\x1f")
        graf = tokens[0]
        sha1, time, subj, refs = (
            tokens[1:] if len(tokens) > 1 else (None, None, None, None)
        )
        return cls(graf, sha1, time, subj, refs)

    def pretty(self, max_graf: int, max_sha1: int, max_time: int) -> str:
        """Return this line formatted and colored, ready for display on the console."""
        graf, sha1 = self._graf, self._sha1
        if sha1 is None:
            return graf
        sha1_pad = (max_graf + max_sha1 - self._graf_len - len(sha1)) * " "
        time_pad = (max_time - len(self._time)) * " "
        return "%s%s%s  %s%s  %s%s" % (
            graf,
            self.sha1,
            sha1_pad,
            self.time,
            time_pad,
            self.subj,
            self.refs,
        )

    @property
    def refs(self) -> str:
        """The colored and formatted refs string.

        Prefixed with padding here to avoid trailing whitespace in commits that have no
        refs.
        """
        refs = self._refs
        if not refs:
            return ""
        return " %s%s%s" % (REFS_COLOR, refs, RESET)

    @property
    def sha1(self) -> str:
        """The colored and formatted SHA1 hash string."""
        return "%s%s%s" % (SHA1_COLOR, self._sha1, RESET)

    @property
    def subj(self) -> str:
        """The colored and formatted commit message string.

        If the message is prefixed with a single-word classifier followed by a colon,
        that classifier gets a distinct color.
        """
        subj = self._subj[:50]
        words = subj.split()
        if not words or not words[0].endswith(":"):
            return subj
        tag = words[0]
        remainder = subj[len(tag) :]
        return "%s%s%s%s" % (TAG_COLOR, tag, RESET, remainder)

    @property
    def time(self) -> str:
        """The colored and formatted relative time string, surrounded by parentheses."""
        return "%s(%s)%s" % (TIME_COLOR, self._time, RESET)

    @property
    def widths(self) -> Tuple[int, int, int]:
        """The (graf_width, sha1_width, time_width) 3-tuple for this line.

        It contains the string length of the graf, sha1, and time fields for this line,
        respectively. The graf string length is calculated after the ANSI color codes
        are stripped from it. These three fields figure in the padding added to fields
        to get them to line up in neat columns on the console.
        """
        if self._sha1 is None:
            return self._graf_len, 0, 0
        return self._graf_len, len(self._sha1), len(self._time)

    @property
    def _graf_len(self) -> int:
        """The length of the graf string after stripping any ANSI color codes."""
        ansi_stripped_graf = self.ansi_regex.sub("", self._graf)
        return len(ansi_stripped_graf)

    @classmethod
    def _condition(cls, line: str) -> str:
        """Return str `line` after removing extraneous information.

        Undesired information includes ' ago' and the ', {n} months' substring in the
        relative time for commits over a year old.
        """
        # --- delimiter \x1b is whitespace in Python 3, so be specific what to strip ---
        line = line.rstrip(" \n")
        # --- Replace (2 years ago) with (2 years) ---
        line = line.replace(" ago", "")
        # --- Replace (2 years, 5 months) with (2 years) ---
        line = cls.months_regex.sub("", line)
        return line
