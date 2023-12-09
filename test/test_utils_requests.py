"""Unit test for module requests of package utils."""
from src.utils.requests import encode_url_params


def test_encode_url_params():
    _params = {
        "key1": "this is a simple string",
        "key2": 2,
        "key3": "ahtlete_id='111'",
        "key4": "ras",
    }

    expected = {
        "key1": "this+is+a+simple+string",
        "key2": 2,
        "key3": "ahtlete_id%3D'111'",
        "key4": "ras",
    }

    encode_url_params(_params)

    assert _params == expected
