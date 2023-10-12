"""Db connection and ops."""

import logging
import os

import redis
import rich.repr

from async_redis.config import Config

log = logging.getLogger("redis-db")


@rich.repr.auto
class Db:
    """Database connection."""

    def __init__(self, ctx: Config):
        """Initialize the db object."""
        log.info("db logger test")
        self.ctx = ctx

    async def connect(self):
        """Connect to redis."""
        redis_auth = os.getenv("REDIS_AUTH", "testpw")

        conn = redis.asyncio.client.Redis(
            host="localhost",
            port=self.ctx.port,
            db=0,
            password=redis_auth,
        )

        await conn.ping()

        return conn
