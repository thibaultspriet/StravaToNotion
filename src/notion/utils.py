"""Utility functions to interact with Notion API."""
from src.const import NOTION_DATABASE_ACTIVITY_ID
from src.notion.client import Client


def get_ids_of_page_activity(
    client: Client, database_id: str, activity_id: str
) -> list[str]:
    """
    Get list of page ids that have the value of Activity ID equals to activity_id.

    :param client:
    :param database_id:
    :param activity_id:
    :return:
    """
    _filter = {
        "property": NOTION_DATABASE_ACTIVITY_ID,
        "rich_text": {"equals": activity_id},
    }

    pages = client.query_database(database_id, filter_=_filter)
    return [page["id"] for page in pages["results"]]
