"""Define the lambda function handler 'controller'."""
import logging
import os
from typing import Any

import boto3

from src.handlers.strava_subscription import callback_validation
from src.types.event import HttpEvent

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def controller(event: HttpEvent, context: dict[str, Any]) -> Any:
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

    if (method == "GET") & (path == "/hello_athlete"):
        return "hello athlete"
    elif (method == "GET") & (path == "/strava_callback"):
        strava_verify_token = os.environ.get("VERIFY_TOKEN")
        if strava_verify_token is None:
            raise RuntimeError("environment variable 'VERIFY_TOKEN' not set")
        return callback_validation(event["queryStringParameters"], strava_verify_token)
    elif (method == "POST") & (path == "/strava_callback"):
        message_body = event["body"]
        sqs = boto3.client("sqs")
        sqs.send_message(
            QueueUrl=os.environ["SQS_URL"], MessageBody=message_body, MessageGroupId="1"
        )
        return {"statusCode": 200, "body": message_body}
    else:
        raise RuntimeError(f"path {path} not implemented")
