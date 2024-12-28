"""Handle authorization to the integration."""
from src.database.interface import DatabaseInterface
from src.notion.client import Client as NotionClient
from src.strava.client import Client
from src.types.oauth import NotionCredentials, StravaCredentials
from src.utils.exceptions import NoSharedPage
from src.workflows import create_notion_database


def add_or_update_strava_oauth(
    strava_credentials: StravaCredentials, user_email: str, database: DatabaseInterface
) -> None:
    """
    Add or update user credentials in the database.

    :param strava_credentials:
    :param user_email:
    :param database:
    :return:
    """
    strava_client = Client(
        strava_credentials["access_token"],
        strava_credentials["refresh_token"],
        int(strava_credentials["expires_at"]),
    )

    athlete_info = strava_client.get_athlete()

    database.add_or_update_strava(strava_credentials, user_email, athlete_info)


def add_or_update_notion(
    credentials: NotionCredentials,
    user_email: str,
    athlete_id: str,
    database: DatabaseInterface,
) -> None:
    """
    Add or update user Notion credentials in the database.

    If it is a new user, create the database of Strava activities in a shared page with the Notion integration.


    :param credentials:
    :param user_email:
    :param athlete_id:
    :param database:
    :return:
    """
    bot_id = credentials["bot_id"]

    database.add_or_update_notion(credentials, user_email, athlete_id)

    # If no database_id : create the Strava activities database and store the id
    notion_client = NotionClient(credentials["access_token"])
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
