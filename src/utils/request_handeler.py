"""Handle requests
"""
import requests
from settings import LOG_PATH
from . import write_log


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


def save_request_data(response: requests.Response, filename: str = "response.html"):
    """Saves the content of the response in a text file

    Args:
        response (Response): the HTTP Response
        filename (str, optional): The path to the file where to save the response.
                                  Defaults to "response.txt".
    """
    with open(filename, "wb") as response_content_file:
        response_content_file.write(response.content)
