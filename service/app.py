import os
from typing import List

import boto3
from chalice.app import Chalice
from pydantic import BaseModel

app = Chalice(app_name="alfred")
s3 = boto3.client("s3")


class Bucket(BaseModel):
    name: str


class BucketList(BaseModel):
    buckets: List[Bucket]


@app.route("/")
def index():
    return {"chalice": "example"}


@app.route("/buckets")
def buckets():
    response = s3.list_buckets()

    names = []
    for bucket in response["Buckets"]:
        names.append(Bucket(name=bucket["Name"]))

    return BucketList(buckets=names).json()


@app.route("/env")
def env():
    chalice_bucket = os.environ.get("CHALICE_BUCKET_NAME")
    return {"env": {"CHALICE_BUCKET_NAME": chalice_bucket}}


@app.lambda_function(name="custom-lambda-chalice")
def custom_lambda_function(event, context):
    return {}
