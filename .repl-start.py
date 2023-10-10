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

if platform.system() == 'Linux':
    libpath = Path(f'{user_home}/.cache/pypoetry/virtualenvs/-c3NNDXsb-py3.11/lib/python3.11/site-packages').as_posix()
else:
    libpath = Path(f'{user_home}/Library/Caches/pypoetry/virtualenvs/async-redis-QD0qW_SU-py3.11/lib/python3.11/site-packages').as_posix()

sys.path.append(libpath)

from tests import test_main
from async_redis import main
from async_redis.main import Config

from faker import Faker

fake = Faker()


