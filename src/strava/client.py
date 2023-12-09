"""Implement a client that handles Strava API calls."""
import json
import os
from datetime import datetime, timedelta
from typing import Optional

import requests

from src.strava.types import DetailedActivity
from src.types.strava import Token
from src.utils.exceptions import MissingEnvironmentVariable


class Client:
    """Strava API manager."""

    base_url = "https://www.strava.com/api/"

    def __init__(
        self, access_token: str, refresh_token: str, expires_at: int, version_label="v3"
    ):
        """
        Init instance.

        :param access_token:
        :param refresh_token:
        :param expires_at:
        :param version_label:
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at
        self.url = f"{self.base_url}{version_label}/"
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")

        for var, name in [
            (self.client_id, "STRAVA_CLIENT_ID"),
            (self.client_secret, "STRAVA_CLIENT_SECRET"),
        ]:
            if var is None:
                raise MissingEnvironmentVariable(name)

    @property
    def authorization(self) -> dict:
        """
        Get the authorization header.

        :return:
        """
        return {"Authorization": f"Bearer {self.access_token}"}

    def refresh_access_token(self, ref=datetime.now()) -> Optional[Token]:
        """
        Refresh access_token if expired.

        Set the instance variables and returns the token.

        :return:
        """
        now = ref - timedelta(seconds=10)  # take a security of few seconds
        if datetime.fromtimestamp(self.expires_at) <= now:
            url = f"{self.url}oauth/token"
            params = {
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            }
            res = requests.post(url, params=params)
            if res.status_code != 200:
                raise Exception(res.text)
            content = json.loads(res.content)
            self.access_token = content["access_token"]
            self.refresh_token = content["refresh_token"]
            self.expires_at = content["expires_at"]
            return {
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
                "expires_at": self.expires_at,
            }

    def get_activity(
        self, activity_id: str, include_all_efforts: bool = False
    ) -> DetailedActivity:
        """
        Call the get activity endpoint.

        :param activity_id:
        :param include_all_efforts:
        :return:
        """
        url = f"{self.url}activities/{activity_id}"
        param = {"include_all_efforts": include_all_efforts}
        self.refresh_access_token()
        res = requests.get(url, params=param, headers=self.authorization)
        if res.status_code != 200:
            raise Exception(res.text)
        else:
            return json.loads(res.content)
