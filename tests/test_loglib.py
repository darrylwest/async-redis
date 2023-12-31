"""Test the log library."""

from rich import inspect

from async_redis.loglib import LogLib
import logging


def test_stream_logger():
    lib = LogLib("test")
    lib.init_stream_logger()
    log = logging.getLogger("test")

    inspect(log)

    log.info("this is a test")
    assert lib.name == "test"
