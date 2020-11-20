# encoding: utf-8

"""Exceptions for scripts."""


class ExecutionError(Exception):
    """Execption for returning non-zero error codes directly to main()."""

    def __init__(self, message, return_code=1):
        self._message = message
        self._return_code = return_code

    def __str__(self):
        return self._message

    @property
    def message(self):
        return self._message

    @property
    def return_code(self):
        return self._return_code
