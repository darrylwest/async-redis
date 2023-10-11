"""Aysnc Redis Tests"""

import pytest
import tomllib
from pathlib import Path

from async_redis import main


def test_version():
    from async_redis import __version__ as vers

    assert vers.startswith("0.1.")
    with Path.open(
        "./pyproject.toml",
        "rb",
    ) as f:
        project = tomllib.load(f)

    assert vers == project["tool"]["poetry"]["version"]


@pytest.mark.asyncio
async def test_start():
    args = []
    await main.start(args)


def test_shutdown():
    main.shutdown()
