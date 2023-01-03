"""Handle requests
"""
import requests
from requests.auth import HTTPBasicAuth
from json import dumps
from settings import LOG_PATH
from . import write_log


def authenticate(username: str, password: str, app_id: str, secret: str) -> str:
    """Gets an access token for future requests

    Args:
        username (str): the username
        password (str): the password
        app_id (str): the id of the app
        secret (str): the secret of the app

    Returns:
        str: The access token
    """

    write_log(f"Authenticating as {username}", LOG_PATH)

    authentication_url = "https://www.reddit.com/api/v1/access_token"

    params = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    headers = {
        "User-agent": 'scrapper 0.1',
    }

    try:
        response = requests.post(
            authentication_url,
            params=params,
            auth=HTTPBasicAuth(app_id, secret),
            headers=headers,
            timeout=5
        )

    # an error occured
    except requests.exceptions.HTTPError as http_error:
        write_log(f"An error has occured: {http_error}", LOG_PATH)
        return None

    # connection was not successfull
    except requests.exceptions.ConnectionError as conn_error:
        write_log(
            f"Couldn't establish a connection to {authentication_url}: {conn_error}",
            LOG_PATH
        )
        return None

    if response.status_code != 200:
        write_log(f"An error has occured - status code: {response.status_code}", LOG_PATH)
        return None

    # try to decode the response
    try:
        # only return the response json if the request succeds
        json_response = response.json()

    except requests.exceptions.JSONDecodeError as json_error:
        write_log(f"Could not decode response into a JSON: {json_error}", LOG_PATH)
        return

    # return the access token
    if "access_token" in json_response:
        write_log("Authenticated successfully", LOG_PATH)
        return json_response["access_token"]


    write_log("An error has occured: Invalid credentials!", LOG_PATH)
    return None



def make_request(post_id: str, access_token: str) -> list:
    """Makes a request to the given url

    Args:
        post_id (str): the id of the post to get the comments from

    Returns:
        list: the HTTP response encoded in json
    """

    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-agent": 'scrapper 0.1',
    }

    url = f"http://oauth.reddit.com/comments/{post_id}?sort=old&threded=false"

    try:
        write_log(f"Connecting to '{url}'", LOG_PATH)

        # make the request to the url
        response = requests.get(
            url,
            headers=headers,
            timeout=5
        )

    # an http error occured
    except requests.exceptions.HTTPError as http_error:
        write_log(f"An error has occured: {http_error}", LOG_PATH)
        return

    # a connection error occured
    except requests.exceptions.ConnectionError as conn_error:
        write_log(f"Unable to connect to '{url}': {conn_error}", LOG_PATH)
        return

    # connection successfull
    write_log(f"Connected to '{url}' successfully", LOG_PATH)

    # couldn't make the request
    if response.status_code != 200:
        write_log(f"An error has occured - status code: {response.status_code}", LOG_PATH)
        return None

    # try to decode
    try:
        return response.json()

    except requests.exceptions.JSONDecodeError as json_error:
        write_log(f"Could not decode response into a JSON: {json_error}", LOG_PATH)
        return


def save_request_data(response: dict, filename: str = "response.json"):
    """Saves the content of the response in a json file

    Args:
        response (dict): the HTTP Response encoded in a dict
        filename (str, optional): The path to the file where to save the response.
                                  Defaults to "response.txt".
    """
    with open(filename, "w", encoding="utf-8") as response_content_file:
        response_content_file.write(dumps(response, indent=4))
