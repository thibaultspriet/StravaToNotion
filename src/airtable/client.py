"""Implement a client that handles airtables API calls."""
import json
from typing import Optional

import requests

from src.airtable.types import (
    ListRecordsQueryParameters,
    Record,
    UpdateRecordBodyParameters,
)
from src.utils.requests import encode_url_params, params_dict_to_str
from src.utils.type_checking import check_keys_of_typed_dict


class Client:
    """Interface to communicate with airtable API."""

    base_url = "https://api.airtable.com/"

    def __init__(self, pat: str, version="v0"):
        """
        Init instance.

        :param pat: personal access token
        :param version: version label of the API
        """
        self.pat = pat
        self.versioned_url = f"{self.base_url}{version}/"

    def base_headers(self) -> dict:
        """
        Return the Authorization header.

        :return:
        """
        return {"Authorization": f"Bearer {self.pat}"}

    def list_records(
        self,
        base_id: str,
        table_id: str,
        query_parameters: Optional[ListRecordsQueryParameters] = None,
    ):
        """
        Call the List records endpoint.

        :param base_id:
        :param table_id:
        :param query_parameters:
        :return:
        """
        check_keys_of_typed_dict(query_parameters, ListRecordsQueryParameters)
        url = f"{self.versioned_url}{base_id}/{table_id}"
        encode_url_params(query_parameters)
        res = requests.get(
            url,
            headers=self.base_headers(),
            params=params_dict_to_str(query_parameters),
        )
        if res.status_code != 200:
            raise Exception(res.text)
        else:
            return json.loads(res.content)

    def update_record(
        self,
        base_id: str,
        table_id: str,
        record_id: str,
        body: UpdateRecordBodyParameters,
    ) -> Record:
        """
        Call the Update record endpoint.

        :param base_id:
        :param table_id:
        :param record_id:
        :param body:
        :return:
        """
        check_keys_of_typed_dict(body, UpdateRecordBodyParameters)
        url = f"{self.versioned_url}{base_id}/{table_id}/{record_id}"
        res = requests.patch(url, json=body, headers=self.base_headers())
        if res.status_code != 200:
            raise Exception(res.text)
        else:
            return json.loads(res.content)
