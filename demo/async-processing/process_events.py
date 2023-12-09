from src.aws_lambda.event import Event
from typing import Any


def controller(event: Event, context: dict[str, Any]) -> Any:
    print(event)
    return "process event"
