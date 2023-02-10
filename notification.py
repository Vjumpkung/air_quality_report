"""A module that keep methods related to line notification."""
import requests
from dotenv import load_dotenv
import urllib
import os

load_dotenv(".env")
REDIRECT_URI_NOTIFY = urllib.parse.quote(os.getenv("REDIRECT_URI_NOTIFY"))
CLIENT_ID_NOTIFY = urllib.parse.quote(os.getenv("CLIENT_ID_NOTIFY"))
CLIENT_SECRET_NOTIFY = urllib.parse.quote(os.getenv("CLIENT_SECRET_NOTIFY"))


def get_access_token(code):
    """Generate access token from the given code."""
    api_url = "https://notify-bot.line.me/oauth/token"
    content_type = "application/x-www-form-urlencoded"

    grant_type = "authorization_code"
    redirect_uri = REDIRECT_URI_NOTIFY
    client_id = CLIENT_ID_NOTIFY
    client_secret = CLIENT_SECRET_NOTIFY
    headers = {'Content-Type': content_type}
    data = {
        "grant_type": grant_type,
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(api_url, headers=headers, data=data)
    return response.json()['access_token']


def send_notification(message, token):
    """Send notification from message anf token provided."""
    url = 'https://notify-api.line.me/api/notify'
    if not token:
        return None
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'Authorization': 'Bearer ' + token}

    response = requests.post(url, headers=headers, data={'message': message})
    return response.json()['status']
