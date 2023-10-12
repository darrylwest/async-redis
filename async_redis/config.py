"""Config Module."""

import logging
import tomllib
from pathlib import Path
from typing import Self

import rich.repr

log = logging.getLogger("async-redis")


@rich.repr.auto
class Config:
    """Configuration for a single redis farm."""

    def __init__(self, name: str, version: str, port: int):
        """Initialize a configuration object for a Redis farm.

        Args:
        ----
            name (str): Name of the Redis farm.
            version (str): Version of the Redis farm.
            port (list[int]): List of Redis port to use.
        """
        self.name = name
        self.version = version
        self.port = port
        self.data = "data"
        self.host = "localhost"
        self.dryrun = False

        log.info(f"init {self}")

    def is_valid(self) -> bool:
        """Return True if the configuration file is valid, else False."""
        errors = []

        if self.port < 1200:
            errors.append("port is missing from config.toml")

        if self.data is None:
            errors.append("data directory is missing from config.toml")

        if not errors:
            log.info("ok.")
            return True

        for error in errors:
            log.error(error)

        log.info(f"Total of {len(errors)} detected.")

        return False

    @classmethod
    def from_toml(cls, toml: dict) -> Self:
        """Parse the toml dict and return a populated configuration object."""
        cfg = cls(
            name=toml.get("name", ""),
            version=toml.get("version", ""),
            port=toml.get("port"),  # type: ignore
        )

        cfg.data = toml.get("data", "data")
        cfg.host = toml.get("host", "localhost")
        cfg.dryrun = toml.get("dryrun", False)

        return cfg

    @classmethod
    def read_config(cls, filename: str | None = None) -> Self:
        """Read and parse the configuration file.

        The configuration toml file is capable of storing multiple configurations for multiple
        farms.  This method reads and parses the entire file and returns the resulting dict.

        Args:
        ----
            filename (str | None, optional): Path to the configuration file. Defaults to None.

        Returns:
        -------
            dict: Parsed configuration.
        """
        if filename is None:
            filename = "./config.toml"

        path = Path(filename)
        with path.open(mode="rb") as file:
            config = tomllib.load(file)

        return cls.from_toml(config["main"])
