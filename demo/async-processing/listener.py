"""Define the lambda function handler 'controller'."""
import logging
import os
from typing import Any
from datetime import datetime
import json


from src.aws_lambda.event import Event
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def controller(event: Event, context: dict[str, Any]) -> Any:
    """
    AWS Lambda Function handler.

    This function is called by the aws lambda runtime
    :param event:
    :param context:
    :return:
    """
    logging.info(event)
    logging.info(context)

    req_context = event.get("requestContext")
    if req_context is None:
        raise RuntimeError("event has not 'requestContext' key")

    _http_info = req_context.get("http")
    if _http_info is None:
        raise RuntimeError("event has not 'requestContext.http' key")

    method = _http_info["method"]
    path = _http_info["path"]

    if (method == "POST") & (path == "/append_queue"):
        now = f"{datetime.now()}"
        sqs = boto3.client('sqs')
        sqs.send_message(
            QueueUrl=os.environ["SQS_URL"],
            MessageBody=now,
            MessageGroupId="1"
        )
        return {
            "statusCode": 200,
            "body": json.dumps(now)
        }

    else:
        raise RuntimeError(f"path {path} not implemented")
