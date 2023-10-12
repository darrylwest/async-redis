"""Config Tests"""


import tomllib
from pathlib import Path
from rich import inspect

from async_redis import config
from async_redis.config import Config


def test_read_config():
    ctx = Config.read_config()
    assert ctx is not None


def test_config_from_toml():
    ctx = Config.read_config("./tests/config.toml")
    assert ctx.name
    assert ctx.is_valid()


def test_bad_config():
    ctx = Config.read_config()

    ctx.port = 100
    ctx.data = None

    inspect(ctx)

    assert ctx.port < 1200
    assert not ctx.is_valid()
