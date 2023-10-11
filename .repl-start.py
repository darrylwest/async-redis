import sys
import os

from pathlib import Path

import time
from datetime import datetime
# import importlib

from rich import inspect
import platform

# print("pid=", os.getpid())

user_home = Path.home().as_posix()

# from pydomkeys.keys import KeyGen
# from faker import Faker
# fake = Faker()

from tests import test_main
from tests.fake_generator import FakeData
from tests.fake_generator import TestUser as User

fake_data = FakeData()

from async_redis import main
from async_redis.main import Config




