from typing import Optional

from pydantic import BaseModel, Field


# TODO find easier way to serialize to proper names
class User(BaseModel):
    id: int
    is_bot: bool
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    language_code: str
    creation_date: Optional[int]

    def to_dynamo(self):
        return {
            "PK": f"USER#{str( self.id )}",
            "SK": "USER",
            # TODO save is bot as a single number instead of string/bool?
            "DATA": f"{self.is_bot}#{self.language_code}",
            "FirstName": self.first_name,
            "LastName": self.last_name,
            "Username": self.username,
            "CreationDate": str(self.creation_date),
        }

    @classmethod
    def from_dynamo(cls, item):
        return cls(
            id=item["PK"].replace("USER#", ""),
            is_bot=item["DATA"].split("#")[0],
            first_name=item["FirstName"],
            last_name=item["LastName"],
            username=item["Username"],
            language_code=item["DATA"].split("#")[1],
            creation_date=int(item["CreationDate"]),
        )

    @classmethod
    def from_telegram(cls, message):
        return cls(
            id=message.from_user.id,
            is_bot=message.from_user.is_bot,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            language_code=message.from_user.language_code,
            creation_date=message.date,
        )


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
