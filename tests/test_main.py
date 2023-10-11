"""Aysnc Redis Tests"""

import pytest
import tomllib
from pathlib import Path

from async_redis import main
from async_redis.main import Config


def test_read_config():
    ctx = main.read_config()
    assert ctx is not None


def test_config_from_toml():
    ctx = main.read_config("./config.toml")
    conf = Config.from_toml(ctx.get("AsyncRedis"))
    assert conf.name
    assert conf.is_valid()


def test_bad_config():
    ctx = main.read_config("./config.toml")
    cfg = ctx.get("BadFarm")

    config = Config.from_toml(cfg)
    assert not config.is_valid()
    config.template = None
    config.port = None
    config.data = None
    assert not config.is_valid()


def test_read_template():
    lines = main.read_template("data/redis-template.conf")
    assert len(lines) == 72


def test_write_config():
    lines = main.read_template("data/redis-template.conf")


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
async def test_main():
    args = []
    await main.start(args)


def test_shutdown():
    main.shutdown()
