"""Db connection and ops tests."""

import pytest
import tomllib
from async_redis.db import Db
from async_redis import config
from async_redis.config import Config

ctx = Config.read_config("tests/config.toml")


def test_instance():
    db = Db(ctx)

    assert db


@pytest.mark.asyncio
async def test_connect():
    db = Db(ctx)
    conn = await db.connect()
    assert conn

    await conn.aclose()
