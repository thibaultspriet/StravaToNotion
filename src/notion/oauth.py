"""Handle the OAuth flow of Notion to allow access to the public integration."""
import base64
import json

import requests


def exchange_token(
    *, code: str, client_id: str, client_secret: str, redirect_uri: str
) -> requests.Response:
    """
    Exchange the temporary code for an access token.

    :param code:
    :param client_id:
    :param client_secret:
    :param redirect_uri:
    :return:
    """
    url = "https://api.notion.com/v1/oauth/token"
    credentials = f"{client_id}:{client_secret}"
    credentials = base64.b64encode(credentials.encode("ascii")).decode("ascii")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {credentials}",
    }
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }

    res = requests.post(url, headers=headers, json=body)
    return json.loads(res.content)
