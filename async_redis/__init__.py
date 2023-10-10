"""Async Redis for tesing concurrent write/reads."""

# keep this in sync with the pypackage.toml file

__version__ = "0.1.0"

from async_redis.loglib import LogLib

LogLib.init_logger()
