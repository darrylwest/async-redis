"""Redis Farm Tests"""

from rich import inspect
import tomllib
from pathlib import Path

from redis_farm import main
from redis_farm.main import Config


def test_read_config():
    ctx = main.read_config("./config.toml")
    assert ctx is not None


def test_config_from_toml():
    ctx = main.read_config("./config.toml")
    conf = Config.from_toml(ctx.get("RedisFarm"))
    assert conf.name
    assert conf.is_valid()


def test_bad_config():
    ctx = main.read_config("./config.toml")
    cfg = ctx.get("BadFarm")

    config = Config.from_toml(cfg)
    assert not config.is_valid()
    config.template = None
    config.ports = None
    config.data = None
    assert not config.is_valid()


def test_read_template():
    lines = main.read_template("data/redis-template.conf")
    assert len(lines) == 72


def test_write_config():
    lines = main.read_template("data/redis-template.conf")
    for port in (2500, 2501):
        filename = f"data/test-{port}.conf"
        main.write_config(filename, port, lines)

        text = [line for line in Path.open(filename, "r")]
        assert len(text) == len(lines)


def test_start():
    ctx = main.read_config("./config.toml")
    config = Config.from_toml(ctx.get("RedisFarm"))
    # main.start(config)
    assert True


def test_status():
    ctx = main.read_config("./config.toml")
    config = Config.from_toml(ctx.get("TestFarm"))
    # main.status(config)
    assert True


def test_stop():
    ctx = main.read_config("./config.toml")
    config = Config.from_toml(ctx.get("TestFarm"))
    # main.stop(config)
    assert True


def test_show_help():
    ctx = main.read_config("./config.toml")
    config = Config.from_toml(ctx.get("TestFarm"))
    main.show_help(config)
    assert True


def test_parse_cli():
    main.parse_cli(["check", "TestFarm"])
    main.parse_cli(["start", "TestFarm"])
    main.parse_cli(["status", "TestFarm"])
    main.parse_cli(["stop", "TestFarm"])
    main.parse_cli(["version", "TestFarm"])
    main.parse_cli(["help", "TestFarm"])
    main.parse_cli(["other", "TestFarm"])


def test_version():
    from redis_farm import __version__ as vers

    assert vers.startswith("0.1.")
    with Path.open(
        "./pyproject.toml",
        "rb",
    ) as f:
        project = tomllib.load(f)

    assert vers == project["tool"]["poetry"]["version"]
