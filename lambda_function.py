"""Define the lambda function handler 'controller'."""
import json
import logging
import os
from time import time
from typing import Any

import boto3

from src.database.airtable import AirtableDatabase
from src.handlers.oauth import add_or_update_notion, add_or_update_strava_oauth
from src.handlers.strava_subscription import callback_validation
from src.notion.oauth import exchange_token
from src.strava.oauth import exchange_code as strava_exchange_token
from src.types.event import HttpEvent

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SQS = boto3.client("sqs")


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
        t0 = time()
        message_body = event["body"]
        SQS.send_message(
            QueueUrl=os.environ["SQS_URL"], MessageBody=message_body, MessageGroupId="1"
        )
        t1 = time()
        print(f"Send message to queue : {t1-t0}s")
        return {"statusCode": 200, "body": message_body}
    elif (method == "POST") & (path == "/notion_oauth_token"):
        client_id = os.environ["NOTION_CLIENT_ID"]
        client_secret = os.environ["NOTION_CLIENT_SECRET"]
        redirect_uri = os.environ["NOTION_CLIENT_REDIRECT_URI"]
        code = json.loads(event["body"])["code"]
        res = exchange_token(
            code=code,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )
        logger.info(res)
        return res
    elif (method == "POST") & (path == "/strava_oauth_token"):
        client_id = os.environ["STRAVA_CLIENT_ID"]
        client_secret = os.environ["STRAVA_CLIENT_SECRET"]
        code = json.loads(event["body"])["code"]
        res = strava_exchange_token(
            code=code,
            client_id=client_id,
            client_secret=client_secret,
        )
        logger.info(res)
        return res
    elif (method == "POST") & (path == "/add_strava_oauth"):
        oauth_credentials = json.loads(event["body"])
        logger.info(oauth_credentials)
        db = AirtableDatabase()
        add_or_update_strava_oauth(
            oauth_credentials["strava"], oauth_credentials["user_email"], db
        )
    elif (method == "POST") & (path == "/add_notion"):
        oauth_credentials = json.loads(event["body"])
        logger.info(oauth_credentials)
        db = AirtableDatabase()
        add_or_update_notion(
            oauth_credentials["notion"],
            oauth_credentials["user_email"],
            oauth_credentials["strava"]["athlete"],
            db,
        )
    else:
        raise RuntimeError(f"path {path} not implemented")
