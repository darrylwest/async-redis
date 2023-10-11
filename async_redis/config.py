"""Config Module."""

import logging
import tomllib
from pathlib import Path
from typing import Self

import rich.repr

# needs to be here rather than __init__
from async_redis.loglib import LogLib

LogLib.init_logger()

log = logging.getLogger("async-redis")


@rich.repr.auto
class Config:
    """Configuration for a single redis farm."""

    def __init__(self, name: str, version: str, template: str, port: int):
        """Initialize a configuration object for a Redis farm.

        Args:
        ----
            name (str): Name of the Redis farm.
            version (str): Version of the Redis farm.
            template (str): Path to the Redis configuration template file.
            port (list[int]): List of Redis port to use.
        """
        self.name = name
        self.version = version
        self.template = template
        self.port = port
        self.data = "data"
        self.host = "localhost"
        self.dryrun = False

        log.info(f"init {self}")

    def is_valid(self) -> bool:
        """Return True if the configuration file is valid, else False."""
        errors = []

        if self.template is None:
            errors.append("template file is missing from config.toml")
        else:
            path = Path(self.template)
            if not path.exists():
                errors.append("template file does not exist")

        if self.port is None:
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
            template=toml.get("template", ""),
            port=toml.get("port"),  # type: ignore
        )

        cfg.data = toml.get("data", "data")
        cfg.host = toml.get("host", "localhost")
        cfg.dryrun = toml.get("dryrun", False)

        return cfg


def read_config(filename: str | None = None) -> dict:
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

    return config


def read_template(template_filename: str) -> list[str]:
    """Process the Redis configuration template for a single farm.

    Args:
    ----
        template_filename (str): Path to the Redis configuration template file.

    Returns:
    -------
        list[str]: List of configuration lines.
    """
    log.info(f"read the template file {template_filename}.")
    path = Path(template_filename)
    lines = []
    with path.open(mode="r", encoding="utf-8") as file:
        while line := file.readline():
            if line == "\n" or line.startswith("#"):
                continue

            lines.append(line.strip())

    return lines


def write_config(filename: str | Path, port: int, lines: list[str]) -> None:
    """Process and write the Redis configuration file for the specified port.

    Args:
    ----
        filename (str | Path): Path to the Redis configuration file.
        port (int): Port number to replace in the configuration lines.
        lines (list[str]): List of configuration lines.
    """
    log.info(f"write config file {filename} for port {port}.")
    sport = str(port)
    path = Path(filename)
    with path.open(mode="w", encoding="utf-8") as file:
        for line in lines:
            rline = line.replace("{{PORT}}", sport)
            file.write(rline)
            file.write("\n")
