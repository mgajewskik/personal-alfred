from typing import List, Protocol, runtime_checkable

from telebot.types import Update, User


# TODO check validity and fill all fields
# protocol classes aim to lower the dependency on the external libraries
# first impression is that this is overengineered for this usecase
# there is no need to type checking here as I can just use the base class
# there is an argument that while testing I am not dependent on the external
# module but still not sure if it is that important
@runtime_checkable
class Bot(Protocol):
    @property
    def user(self) -> User:
        ...

    def process_new_updates(self, updates: List[Update]):
        ...


@runtime_checkable
class DBRepository(Protocol):
    def get(self):
        ...

    def add(self):
        ...
