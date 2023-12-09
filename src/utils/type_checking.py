"""Utility functions to check type of function parameters."""
from src.utils.exceptions import InvalidTypedDictParameter


def check_keys_of_typed_dict(parameter: dict, typed_dict: type) -> None:
    """
    Check if a parameter expected as a TypedDict contains an unexpected key.

    Raise an InvalidTypedDictParameter in case an invalid key is encountered.

    :param parameter: parameter to check
    :param typed_dict: a TypedDict class
    :return:
    """
    expected_keys = typed_dict.__annotations__.keys()
    if parameter:
        for key in parameter.keys():
            if key not in expected_keys:
                raise InvalidTypedDictParameter(key, typed_dict)
