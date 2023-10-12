"""Db connection and ops tests."""

import pytest
from rich import inspect

from async_redis.db import Db
from async_redis.config import Config

ctx = Config.read_config("tests/config.toml")


def test_instance():
    db = Db(ctx)
    assert db
    assert db.client is None


@pytest.mark.asyncio
async def test_connect():
    db = Db(ctx)
    client = await db.connect()
    inspect(client)
    assert client is not None

    dbsize = await client.dbsize()
    assert dbsize >= 0
    
    for _ in range(10):
        resp = await client.ping()
        inspect(resp)
        assert resp

    await client.aclose()

@pytest.mark.asyncio
async def test_pipeline():
    db = Db(ctx)
    client = await db.connect()

    await client.aclose()
