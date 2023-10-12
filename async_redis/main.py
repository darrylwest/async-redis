"""Main project logic."""

import logging

from async_redis import config
from async_redis.config import Config
# needs to be here rather than __init__
from async_redis.loglib import LogLib

LogLib.init_loggers()

log = logging.getLogger("async-redis")


async def start(args: list) -> None:
    """Start the application."""
    log.info(f"start the application with args: {args}")
    cfg = config.read_config()
    ctx = Config.from_toml(cfg["AsyncRedis"])
    log.info(f"{ctx}")

def shutdown() -> None:
    """Shutdown the application."""
    log.info("application shutdown...")
