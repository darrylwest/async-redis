#!/usr/bin/env python3
# dpw@plaza.localdomain
# 2023-10-11 17:36:50

from rich import inspect
from dataclasses import dataclass
from pydomkeys.keys import KeyGen
from faker import Faker
from time import time
from datetime import datetime, timezone


@dataclass
class TestUser:
    key: str
    created_at: float
    updated_at: float
    first_name: str
    last_name: str
    email: str
    phone: str
    birth_year: int


class FakeData:
    def __init__(self):
        self.fake = Faker()
        self.keygen = KeyGen.create("TU")
        self.today = datetime.now(tz=timezone.utc)

    def birth_year(self, min_age: int = 20, max_age: int = 100) -> int:
        return self.today.year - self.fake.random_int(min_age, max_age)

    def phone(self) -> str:
        return f"{self.fake.random_int(100,999)}-{self.fake.random_int(100,999)}-{self.fake.random_int(1000, 9999)}"

    def create_user(self) -> TestUser:
        now = time()
        key = self.keygen.route_key()
        fname = self.fake.first_name()
        lname = self.fake.last_name()
        suffix = f"{self.fake.random_digit_above_two()}{self.fake.random_digit()}"
        email = f"{fname.lower()}.{lname.lower()}-{suffix}@{self.fake.domain_name()}"

        test_user = TestUser(
            key=key,
            created_at=now,
            updated_at=now,
            first_name=fname,
            last_name=lname,
            email=email,
            phone=self.phone(),
            birth_year=self.birth_year(),
        )

        return test_user

    def create_users(self, count: int = 10):
        """a generator to create many users"""
        return (self.create_user() for _n in range(count))


def main() -> None:
    fake_data = FakeData()
    gen = fake_data.create_users(2)
    user = next(gen)
    inspect(user)
    user = next(gen)
    inspect(user)


if __name__ == "__main__":
    main()
