"""Utility functions to deal with the requests library."""
from urllib.parse import quote_plus


def encode_url_params(params: dict) -> None:
    """
    Encode string parameters.

    Changes are made in place.
    :param params:
    :return:
    """
    if params:
        for key, val in params.items():
            if isinstance(val, str):
                params[key] = quote_plus(val, safe="'")


def params_dict_to_str(params: dict) -> str:
    """
    Return a string of url parameters based on a dict.

    It is used to prevent the library requests to url encode already encoded parameters.
    :param params:
    :return:
    """
    return "&".join(f"{k}={v}" for k, v in params.items())
