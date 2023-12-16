"""Handle the OAuth flow of Notion to allow access to the public integration."""
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
    url = "https://www.notion.so/v1/oauth/token"
    headers = {"Content-Type": "application/json"}
    body = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    res = requests.post(url, headers=headers, json=body)
    return res.content
