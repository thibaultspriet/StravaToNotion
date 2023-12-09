"""Define entrypoint of Lambda function."""
from typing import Any

from src.aws_lambda.event import Event


def controller(event: Event, context: dict[str, Any]) -> Any:
    """
    Entrypoint of Lambda function.

    :param event:
    :param context:
    :return:
    """
    print(event)
    return "process event"
