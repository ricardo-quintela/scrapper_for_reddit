"""Scrape a post from reddit and generate a script
"""
import getpass
from settings import APP_ID, SECRET, LOG_PATH
from utils import authenticate, make_request, save_request_data, extract_id, save_comments_md, extract_bodies
from utils import create_log_file, write_log
from utils import analyze_data

def scrape_post(username: str, url: str):
    """Scrapes a post from reddit and generates a MarkDown script

    Args:
        username (str): the username from reddit
        url (str): the post url
    """
    # separate the username and url and get the pasword
    password = getpass.getpass(f"Password for username {username}: ")

    create_log_file(LOG_PATH)

    # extract the post id from the url
    post_id = extract_id(url)

    access_token = authenticate(username, password, APP_ID, SECRET)

    if access_token is None:
        return

    response = make_request(post_id, access_token)

    if response is None:
        return

    save_request_data(response, f"{post_id}.json")

    # extract the comments form the response
    data = extract_bodies(response)

    if data is None:
        return

    analyze_data(data[1])

    # save the comments to md
    save_comments_md(data, f"{post_id}.md")

    # success
    write_log(f"Data saved as {post_id}.md", LOG_PATH)
