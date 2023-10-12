"""Db connection and ops tests."""

import pytest
import tomllib
from async_redis.db import Db
from async_redis import config
from async_redis.config import Config

def test_instance():
    conf = config.read_config()
    ctx = Config.from_toml(conf['TestAsync'])

    assert ctx.is_valid()
    db = Db(ctx)

    assert db
