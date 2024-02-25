"""Handle the OAuth flow for Strava."""
import json

import requests


def exchange_code(
    *, code: str, client_id: str, client_secret: str
) -> requests.Response:
    """
    Exchange the code received by the client with Strava to receive access token and refresh token.

    :param code: code received by the client
    :param client_id: client id of the Strava app
    :param client_secret: client secret of the Strava app
    :return:
    """
    url = "https://www.strava.com/oauth/token"

    body = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }

    res = requests.post(url, json=body)
    return json.loads(res.content)
