"""Define the entrypoint of Lambda function."""
import json
import logging
from typing import Any

from src.database.airtable import AirtableDatabase
from src.handlers.actions import CreateActivity, UpdateActivity
from src.types.event import SqsEvent

logger = logging.getLogger()
logger.setLevel(logging.INFO)

actions = {"create.activity": CreateActivity, "update.activity": UpdateActivity}


def controller(event: SqsEvent, context: dict[str, Any]) -> Any:
    """
    Entrypoint for Lambda function.

    :param event:
    :param context:
    :return:
    """
    if event:
        batch_item_failures = []
        sqs_batch_response = {}
        logger.info(event)
        for record in event["Records"]:
            message_id = record["messageId"]
            logger.info(f"processing message : {message_id} ...")
            body = json.loads(record["body"])
            action = f"{body['aspect_type']}.{body['object_type']}"
            concrete_action = actions.get(action)
            if concrete_action is not None:
                owner = str(body["owner_id"])
                object_id = str(body["object_id"])
                database_client = AirtableDatabase()
                try:
                    res = concrete_action(owner, object_id, database_client).run()
                    logger.info(res)
                except Exception as e:
                    logger.exception(
                        f"exception encountered while processing {message_id}"
                    )
                    batch_item_failures.append({"itemIdentifier": record["messageId"]})
            else:
                logger.warning(f"action {concrete_action} not implemented yet")
                batch_item_failures.append({"itemIdentifier": record["messageId"]})
        sqs_batch_response["batchItemFailures"] = batch_item_failures
        return sqs_batch_response
