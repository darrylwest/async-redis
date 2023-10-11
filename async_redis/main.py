"""Main project logic."""

import logging
from pathlib import Path

from async_redis import config
from async_redis.config import Config
# needs to be here rather than __init__
from async_redis.loglib import LogLib

LogLib.init_logger()

log = logging.getLogger("async-redis")


async def start(args: list) -> None:
    """Start the application."""
    log.info(f"start the application with args: {args}")
    cfg = config.read_config()
    ctx = Config.from_toml(cfg["AsyncRedis"])
    log.info(f"{ctx}")

    # TODO(dpw): move this inside config
    data_path = Path(f"{ctx.data}/redis-{ctx.port}.conf")
    lines = config.read_template(ctx.template)
    config.write_config(data_path, ctx.port, lines)


def shutdown():
    """Shutdown the application."""
    log.info("application shutdown...")
