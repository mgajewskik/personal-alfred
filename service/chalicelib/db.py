import boto3

from .models import User
from .settings import APISettings


def get_dynamodb(settings: APISettings) -> boto3.resource:
    return boto3.resource("dynamodb", region_name=settings.AWS_REGION)


# https://www.cosmicpython.com/book/chapter_02_repository.html

# not really suitable for working specifically with single table in dynamodb
# might be more useful for trying to be dlexible with many databases
# class DynamoDBTableRepository:
#     def __init__(self, table: boto3.resource.Table, model: BaseModel):
#         # table should be more universal? conn?
#         self.table = table
#         self.model = model
#
#     def get(self, key: dict) -> dict:
#         response = self.table.get_item(Key=key)
#         return response["Item"]


# TODO some of the functions can be joined together
# TODO add models to data structures
class Dynamo:
    def __init__(self, settings: APISettings):
        self.dynamodb = get_dynamodb(settings)
        self.settings = settings
        self.db = self.dynamodb.Table(self.settings.USERS_TABLE_NAME)

    # PK
    def get_user(self, user_id: int):
        # TODO add error handling
        response = self.db.get_item(Key={"PK": f"USER#{str(user_id)}", "SK": "USER"})
        return User.from_dynamo(response["Item"])

    # GSI1
    def get_users(self, is_bot: bool = None, language_code: str = None):
        ...

    # GSI2
    def get_users_by_creation_date(self, from_date: int, to_date: int):
        ...

    # GSI1
    def get_user_messages(self, user_id: int, msg_id: int = None, type: str = None):
        ...

    # GSI2
    def get_user_messages_by_date(self, user_id: int, from_date: int, to_date: int):
        ...

    # PK
    def add_user(self, user) -> bool:
        # TODO add error handling
        # TODO add logic not to overwrite user
        response = self.db.put_item(Item=user.to_dynamo())
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return True
        return False

    # PK
    def add_message(self, message):
        self.db.put_item(Item=message.to_dynamo())
