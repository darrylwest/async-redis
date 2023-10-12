"""Db connection and ops tests."""

import asyncio
import pytest
from rich import print
import json

from tests.fake_generator import FakeData

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
    print(client)
    assert client is not None

    dbsize = await client.dbsize()
    assert dbsize >= 0

    for _ in range(5):
        resp = await client.ping()
        await asyncio.sleep(0.002)
        assert resp

    await client.aclose()


@pytest.mark.asyncio
async def test_pipeline():
    fake = FakeData()
    count = 10
    users = fake.create_users(count)

    db = Db(ctx)
    client = await db.connect()

    dbsize = await client.dbsize()

    for user in users:
        pipe = client.pipeline(transaction=True)
        jstr = json.dumps(user.__dict__)
        eix = f"eIX{user.email}"
        pipe.set(user.key, jstr)
        pipe.set(eix, user.key)

        resp = await pipe.execute()
        # inspect(resp)
        assert all(resp)  # all should be true

        exists = await client.exists(user.key)
        assert exists

        mstr = await client.get(user.key)
        # inspect(mstr)

    new_dbsize = await client.dbsize()
    assert new_dbsize == dbsize + (count * 2)

    keys = []
    it = client.scan_iter(match="TU*", count=10)
    async for key in it:
        keys.append(key)
        jstr = await client.get(key)
        udct = json.loads(jstr)
        assert udct
        assert udct["key"]
        print(key, udct)

        if len(keys) == 10:
            break

    assert len(keys) >= count
    await asyncio.sleep(0.02)

    await client.aclose()
