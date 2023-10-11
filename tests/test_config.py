"""Config Tests"""


import tomllib
from pathlib import Path

from async_redis import config
from async_redis.config import Config


def test_read_config():
    ctx = config.read_config()
    assert ctx is not None


def test_config_from_toml():
    ctx = config.read_config("./config.toml")
    conf = Config.from_toml(ctx.get("AsyncRedis"))
    assert conf.name
    assert conf.is_valid()


def test_bad_config():
    ctx = config.read_config("./config.toml")
    cfg = ctx.get("BadFarm")

    conf = Config.from_toml(cfg)
    assert not conf.is_valid()
    conf.template = None
    conf.port = None
    conf.data = None
    assert not conf.is_valid()


def test_read_template():
    lines = config.read_template("data/redis-template.conf")
    assert len(lines) == 72


def test_write_config():
    lines = config.read_template("data/redis-template.conf")


def test_version():
    from async_redis import __version__ as vers

    assert vers.startswith("0.1.")
    with Path.open(
        "./pyproject.toml",
        "rb",
    ) as f:
        project = tomllib.load(f)

    assert vers == project["tool"]["poetry"]["version"]
