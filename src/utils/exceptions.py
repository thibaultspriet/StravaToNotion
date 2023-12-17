"""Define custom exceptions."""
from typing import Any


class InternalException(Exception):
    """Base class for all user defined Exception."""

    pass


class InvalidTypedDictParameter(InternalException):
    """Raised when a parameter expected as a TypedDict contains an unexpected key."""

    def __init__(self, unexpected_key: Any, typed_dict: type):
        """
        Init instance.

        :param unexpected_key:
        :param typed_dict:
        """
        super().__init__(
            f"unexpected key : {unexpected_key} for TypedDict {typed_dict}"
        )


class MissingEnvironmentVariable(InternalException):
    """Raised when a required environment variable is not set."""

    def __init__(self, env_variable: str):
        """
        Init instance.

        :param env_variable:
        """
        super().__init__(f"environment variable '{env_variable}' is not set.")


class NoSharedPage(InternalException):
    """Raised if any page is shared with the Notion integration."""

    def __init__(self, bot_id: str):
        """
        Init instance.

        :param bot_id:
        """
        super().__init__(f"Integration of bot_id : {bot_id} is shared with any page.")
