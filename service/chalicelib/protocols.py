from typing import List, Protocol

from telebot.types import Update, User


# TODO check validity and fill all fields
# protocol classes aim to lower the dependency on the external libraries
class Bot(Protocol):
    @property
    def user(self) -> User:
        ...

    def process_new_updates(self, updates: List[Update]):
        ...
