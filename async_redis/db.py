"""Db connection and ops."""

import logging
import os

import redis.asyncio as redis
import rich.repr

from async_redis.config import Config

log = logging.getLogger("redis-db")


@rich.repr.auto
class Db:
    """Database connection."""

    def __init__(self, ctx: Config):
        """Initialize the db object."""
        self.ctx = ctx
        self.client = None

    async def connect(self):
        """Connect to redis."""
        if self.client is None:
            log.info("create the db client")
            redis_auth = os.getenv("REDIS_AUTH", "testpw")

            self.client = redis.Redis(
                host="localhost",
                port=self.ctx.port,
                db=0,
                password=redis_auth,
                protocol=3,
            )

            await self.client.ping()

        return self.client

    async def ping(self) -> bool:
        """Ping the client connection."""
        conn = await self.connect()
        pong = await conn.ping()
        return pong
