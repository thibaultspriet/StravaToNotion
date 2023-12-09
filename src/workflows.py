"""Define functions that interact with different entities."""
import json
import logging

from src.const import NOTION_DATABASE_PROPERTIES_TEMPLATE
from src.database.interface import DatabaseInterface
from src.strava.client import Client as StravaClient

logger = logging.getLogger()


def refresh_strava_token(
    athlete_id: str, strava_client: StravaClient, database_client: DatabaseInterface
) -> None:
    """
    Refresh the strava tokens of an athlete.

    Generate new tokens with the Strava API and stores the new tokens in the database

    :param athlete_id:
    :param strava_client:
    :param database_client:
    :return:
    """
    token = strava_client.refresh_access_token()
    if token is not None:
        logger.debug(f"refreshing token of athlete {athlete_id}")
        token["expires_at"] = str(token["expires_at"])
        database_client.update_strava_credentials(athlete_id, token)
    else:
        logger.debug(f"token of athlete {athlete_id} still valid")


def strava_activity_to_notion_properties(activity: dict) -> dict:
    """
    Interface between Strava activity data and Notion properties data.

    :param activity:
    :return:
    """
    mapping = {
        "name": activity["name"],
        "description": activity["description"],
        "type": activity["sport_type"],
        "calories": activity["calories"],
        "start": activity["start_date"],
        "activity_id": activity["id"],
        "avg_speed": activity["average_speed"],
        "max_speed": activity["max_speed"],
        "total_elevation_gain": activity["total_elevation_gain"],
        "external_id": activity["external_id"],
        "upload_id": activity["upload_id"],
        "time": activity["moving_time"],
        "distance": activity["distance"],
    }

    return json.loads(NOTION_DATABASE_PROPERTIES_TEMPLATE.substitute(**mapping))
