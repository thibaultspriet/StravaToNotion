"""Unit test module for the type_checking.py module."""
from typing import TypedDict

import pytest

from src.utils.exceptions import InvalidTypedDictParameter
from src.utils.type_checking import check_keys_of_typed_dict


def test_type_checking():
    """Test the check_keys_of_typed_dict."""

    class _TestDict(TypedDict):
        """Test dict."""

        a: int
        b: str

    with pytest.raises(InvalidTypedDictParameter):
        check_keys_of_typed_dict({"c": 3}, _TestDict)

    assert check_keys_of_typed_dict({"a": 3, "b": "str"}, _TestDict) is None
