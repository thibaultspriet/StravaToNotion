"""Define a class Client to interact with Notion API."""
import json

import requests


class Client:
    """Client to interact with Notion API."""

    base_url = "https://api.notion.com/"

    def __init__(self, access_token: str, version="2022-06-28"):
        """
        Init instance.

        :param access_token:
        :param version:
        """
        self.access_token = access_token
        self.version = version

    @property
    def header(self) -> dict:
        """
        Returns base headers.

        :return:
        """
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Notion-Version": self.version,
        }

    def create_page(
        self,
        parent_id: str,
        properties: dict,
        children: list = None,
        icon: dict = None,
        cover: dict = None,
        to_database: bool = True,
    ) -> dict:
        """
        Create a page.

        The page can be created as a simple page or as an item of a database.
        :param parent_id:
        :param properties:
        :param children:
        :param icon:
        :param cover:
        :param to_database:
        :return:
        """
        parent = "database_id" if to_database else "page_id"
        url = f"{self.base_url}v1/pages"
        body = {
            "parent": {parent: parent_id},
            "properties": properties,
        }

        for k, v in {"children": children, "icon": icon, "cover": cover}.items():
            if v is not None:
                body[k] = v

        res = requests.post(url, headers=self.header, json=body)
        if res.status_code != 200:
            raise Exception(res.text)
        else:
            return json.loads(res.content)

    def query_database(
        self,
        database_id: str,
        filter_properties: list[str] = None,
        filter_: dict = None,
        sorts: list = None,
        start_cursor: str = None,
        page_size: int = None,
    ) -> dict:
        """
        Call the Query database endpoint.

        :param database_id:
        :param filter_properties:
        :param filter_:
        :param sorts:
        :param start_cursor:
        :param page_size:
        :return:
        """
        url = f"{self.base_url}v1/databases/{database_id}/query"
        params = None
        body = {}
        if filter_properties is not None:
            params = "&".join(
                [f"filter_properties={prop}" for prop in filter_properties]
            )
        for k, v in {
            "filter": filter_,
            "sorts": sorts,
            "start_cursor": start_cursor,
            "page_size": page_size,
        }.items():
            if v is not None:
                body[k] = v
        res = requests.post(url, headers=self.header, json=body, params=params)
        if res.status_code != 200:
            raise Exception(res.text)
        else:
            return json.loads(res.content)

    def update_page_properties(
        self,
        page_id: str,
        properties: dict = None,
        archived: bool = None,
        icon: dict = None,
        cover: dict = None,
    ) -> dict:
        """
        Update properties of an existing page.

        :param page_id:
        :param properties:
        :param archived:
        :param icon:
        :param cover:
        :return:
        """
        url = f"{self.base_url}v1/pages/{page_id}"
        body = {}
        for k, v in {
            "properties": properties,
            "archived": archived,
            "icon": icon,
            "cover": cover,
        }.items():
            if v is not None:
                body[k] = v
        res = requests.patch(url, headers=self.header, json=body)
        if res.status_code != 200:
            raise Exception(res.text)
        else:
            return json.loads(res.content)

    def search(
        self,
        query: str = None,
        sort: dict = None,
        _filter: dict = None,
        start_cursor: str = None,
        page_size: int = None,
    ) -> dict:
        """
        Call the search endpoint.

        This endpoint allows retrieving pages and databases shared with the integration.
        :param query:
        :param sort:
        :param _filter:
        :param start_cursor:
        :param page_size:
        :return:
        """
        url = f"{self.base_url}v1/search"
        body = {}
        for k, v in {
            "query": query,
            "sort": sort,
            "filter": _filter,
            "start_cursor": start_cursor,
            "page_size": page_size,
        }.items():
            if v is not None:
                body[k] = v
        res = requests.post(url, headers=self.header, json=body)
        if res.status_code != 200:
            raise Exception(res.text)
        else:
            return json.loads(res.content)

    def create_database(self, parent: dict, title: list, properties: dict) -> dict:
        """
        Call the database endpoint to create a new one.

        :param parent:
        :param title:
        :param properties:
        :return:
        """
        url = f"{self.base_url}v1/databases"
        body = {"parent": parent, "title": title, "properties": properties}
        res = requests.post(url, headers=self.header, json=body)
        if res.status_code != 200:
            raise Exception(res.text)
        else:
            return json.loads(res.content)
