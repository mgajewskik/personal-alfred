from typing import Optional

from pydantic import BaseModel, Field

# seems like this is a proper type for the bot event
# from telebot.types import Update

# TODO do I even need those models now?
# nothing to deserialize here


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: str
    language_code: str


class Chat(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    username: str
    type: str


class Message(BaseModel):
    message_id: int
    from_field: User = Field(..., alias="from")
    chat: Chat
    date: int
    text: str


class BotEvent(BaseModel):
    update_id: int
    message: Message
