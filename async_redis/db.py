"""Db connection and ops."""

import logging

from async_redis.config import Config

log = logging.getLogger("redis-db")

import rich.repr

@rich.repr.auto
class Db:
   """Database connection."""
   def __init__(self, ctx: Config):
        log.info('db logger test')
        self.ctx = ctx