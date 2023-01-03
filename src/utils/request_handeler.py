"""Handle requests
"""
import requests
from requests.auth import HTTPBasicAuth
from settings import LOG_PATH
from . import write_log



def save_request_data(response: requests.Response, filename: str = "response.html"):
    """Saves the content of the response in a text file

    Args:
        response (Response): the HTTP Response
        filename (str, optional): The path to the file where to save the response.
                                  Defaults to "response.txt".
    """
    with open(filename, "wb") as response_content_file:
        response_content_file.write(response.content)



def authenticate(username: str, password: str, app_id: str, secret: str) -> requests.Response:
    """Gets an access token for future requests

    Args:
        username (str): the username
        password (str): the password
        app_id (str): the id of the app
        secret (str): the secret of the app

    Returns:
        dict: The HTTP Response of the post request containing the access token
    """

    authentication_url = "https://www.reddit.com/api/v1/access_token"

    params = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    headers = {
        "User-agent": 'scrapper 0.1',
    }

    response = requests.post(
        authentication_url,
        params=params,
        auth=HTTPBasicAuth(app_id, secret),
        headers=headers,
        timeout=5
    )

    return response.json()


def make_request(url: str) -> requests.Response:
    """Makes a request to the given url

    Args:
        url (str): the url to make the request to

    Returns:
        Response: the HTTP response
    """

    try:
        write_log(f"Connecting to '{url}'", LOG_PATH)

        # make the request to the url
        response = requests.get(url, timeout=10)

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

    return response
