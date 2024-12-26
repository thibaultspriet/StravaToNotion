"""Handle authorization to the integration."""
from src.database.interface import DatabaseInterface
from src.notion.client import Client as NotionClient
from src.strava.client import Client
from src.types.oauth import OauthCredentials
from src.utils.exceptions import NoSharedPage
from src.workflows import create_notion_database


def add_or_update_user(
    oauth_credentials: OauthCredentials, database: DatabaseInterface
) -> None:
    """
    Add or update user credentials in the database.

    If it is a new user, create the database of Strava activities in a shared page with the Notion integration.

    :param oauth_credentials:
    :param database:
    :return:
    """
    user_email = oauth_credentials["user_email"]
    athlete_id = oauth_credentials["strava"]["athlete"]
    bot_id = oauth_credentials["notion"]["bot_id"]

    strava_client = Client(
        oauth_credentials["strava"]["access_token"],
        oauth_credentials["strava"]["refresh_token"],
        int(oauth_credentials["strava"]["expires_at"]),
    )

    athlete_info = strava_client.get_athlete()

    database.add_or_update_user(oauth_credentials, athlete_info)

    # If no database_id : create the Strava activities database and store the id
    notion_client = NotionClient(oauth_credentials["notion"]["access_token"])
    database_id = database.get_notion_database_id(user_email, athlete_id, bot_id)
    if database_id is None:
        pages = notion_client.search(_filter={"value": "page", "property": "object"})[
            "results"
        ]
        if len(pages) == 0:
            raise NoSharedPage(bot_id)
        parent_page_id = pages[0]["id"]
        new_db_id = create_notion_database(notion_client, parent_page_id)
        database.update_database_id(user_email, athlete_id, bot_id, new_db_id)
