#!/usr/bin/env python3
# dpw@plaza.localdomain
# 2023-10-12 21:18:58


import asyncio
import sys
from time import perf_counter
from rich import print, inspect
import json
from tests.fake_generator import FakeData

from async_redis.db import Db
from async_redis.config import Config
import redis.asyncio as redis


async def insert(client: redis.Redis, user) -> bool:
    jstr = json.dumps(user.__dict__)
    eix = f"eIX{user.email}"
    pipe = client.pipeline(transaction=True)
    pipe.set(user.key, jstr)
    pipe.set(eix, user.key)
    resp = await pipe.execute()

    return all(resp)


async def create_models(client: redis.Redis, count: int = 1000):
    fake = FakeData()
    users = fake.create_users(count)

    print(f"client: {client}, create and insert {count} new users.")

    pong = await client.ping()
    assert pong

    t0 = perf_counter()
    for user in users:
        resp = await insert(client, user)
        assert resp

    t1 = perf_counter()
    print(f"elapsed {t1 - t0} seconds")

    dbsize = await client.dbsize()
    print(f"dbsize: {dbsize}")


async def main(args: list) -> None:
    ctx = Config.read_config()
    db = Db(ctx)

    if "--insert" in args:
        try:
            client = await db.connect()
            await create_models(client)
        finally:
            await client.aclose()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
